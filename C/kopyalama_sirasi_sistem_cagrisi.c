#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <string.h>

#ifndef ORIG_RAX
#define ORIG_RAX 15  // x86_64 mimarisi için
#endif

void copy_file() {
    FILE *src, *dest;
    char buffer[1024];
    size_t bytes;

    // Kaynak ve hedef dosyaları aç
    src = fopen("ahmet.txt", "r");
    if (src == NULL) {
        perror("Kaynak dosya açılamadı");
        return;
    }

    dest = fopen("ahmet_kopyalanan.txt", "w");
    if (dest == NULL) {
        perror("Hedef dosya açılamadı");
        fclose(src);
        return;
    }

    // Dosya içeriğini kopyala
    while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        fwrite(buffer, 1, bytes, dest);
    }

    // Dosyaları kapat
    fclose(src);
    fclose(dest);
}

int main() {
    pid_t child;
    long orig_rax;
    int status;
    struct user_regs_struct regs;

    child = fork();

    if (child == 0) {
        // Çocuk işlem (trace edilen işlem)
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execl("/bin/cat", "cat", "ahmet.txt", NULL);  // Kopyalama işlemi sırasında izlenecek işlem
    } else {
        // Ana işlem (izleyici)
        while (1) {
            wait(&status);  // Çocuğun sistem çağrısını bekle
            if (WIFEXITED(status))  // Çıkış yaptıysa döngüden çık
                break;

            orig_rax = ptrace(PTRACE_PEEKUSER, child, sizeof(long) * ORIG_RAX, NULL);

            const char *syscall_names[] = {
                [0] = "read",
                [1] = "write",
                [2] = "open",
                [3] = "close",
                [257] = "openat",
                [62] = "kill",
                [60] = "exit"
            };

            printf("Sistem çağrısı: %s (%ld)\n",
                   syscall_names[orig_rax] ? syscall_names[orig_rax] : "Bilinmeyen",
                   orig_rax);

            ptrace(PTRACE_SYSCALL, child, NULL, NULL);  // Devam et
        }
    }

    // Dosya kopyalama işlemini çağır
    copy_file();

    return 0;
}

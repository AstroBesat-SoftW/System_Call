#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/syscall.h>

#ifndef ORIG_RAX
#define ORIG_RAX 15  // x86_64 mimarisi için
#endif

int main() {
    pid_t child;
    long orig_rax;
    int status;
    struct user_regs_struct regs;

    child = fork();

    if (child == 0) {
        // Çocuk işlem (trace edilen işlem)
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        execl("/bin/ls", "ls", NULL);  // İzlenecek işlem (örneğin ls komutu)
    } else {
        // Ana işlem (izleyici)
        while (1) {
            wait(&status);  // Çocuğun sistem çağrısını bekle
            if (WIFEXITED(status))  // Çıkış yaptıysa döngüden çık
                break;

            orig_rax = ptrace(PTRACE_PEEKUSER, child, sizeof(long) * ORIG_RAX, NULL);
            // sonra ekledim altı linux sistem çağrıları
  const char *syscall_names[] = {
    [0] = "read (Dosyadan veri okuma)",
    [1] = "write (Dosyaya veri yazma)",
    [2] = "open (Dosya açma)",
    [3] = "close (Açık dosya tanıtıcısını kapatma)",
    [4] = "stat (Dosya hakkında bilgi alır)",
    [5] = "fstat (Açık dosya tanıtıcısından dosya bilgisi alır)",
    [6] = "lstat (Sembolik bağlantıların bilgilerini alır)",
    [7] = "poll (Dosya tanıtıcılarını izler, I/O için hazır olup olmadıklarını kontrol eder)",
    [8] = "lseek (Dosya işaretçisini belirli bir konuma taşır)",
    [9] = "mmap (Bellek bölgesi eşleme - dosya veya cihaz belleğini adres alanına ekler)",
    [10] = "mprotect (Bellek bölgesi için izinleri ayarlar)",
    [11] = "munmap (Bellek eşlemeyi kaldırır)",
    [12] = "brk (Heap bellek alanını genişletir veya daraltır)",
    [13] = "rt_sigaction (Sinyal işleyicisi ayarlar)",
    [14] = "rt_sigprocmask (Sinyal maskelemesi ayarlar)",
    [15] = "rt_sigreturn (Sinyal işleyicisini döner)",
    [16] = "ioctl (Aygıt kontrolü yapar)",
    [17] = "pread64 (Belirli bir konumdan dosya okur)",
    [18] = "pwrite64 (Belirli bir konumda dosyaya yazar)",
    [19] = "readv (Birden fazla veri bloğunu okur)",
    [20] = "writev (Birden fazla veri bloğunu yazar)",
    [21] = "access (Dosya veya dizine erişimi kontrol eder)",
    [22] = "pipe (İki süreç arasında iletişim için pipe oluşturur)",
    [23] = "select (Birden fazla dosya tanıtıcısını izler)",
    [24] = "sched_yield (CPU'yu bırakır, diğer işlemleri çalıştırmaya izin verir)",
    [25] = "mremap (Bellek eşlemesini yeniden boyutlandırır)",
    [26] = "msync (Bellek eşlemesini diske yazar)",
    [27] = "mincore (Bellek sayfasının yüklü olup olmadığını kontrol eder)",
    [28] = "madvise (Bellek kullanımı için öneride bulunur)",
    [29] = "shmget (Paylaşılan bellek segmenti oluşturur veya erişir)",
    [30] = "shmat (Paylaşılan bellek segmentini işlem adres alanına ekler)",
    [31] = "shmctl (Paylaşılan bellek kontrol işlemleri yapar)",
    [32] = "dup (Dosya tanıtıcısını kopyalar)",
    [33] = "dup2 (Dosya tanıtıcısını belirli bir tanıtıcıya kopyalar)",
    [34] = "pause (Bir sinyal alınana kadar süreci durdurur)",
    [35] = "nanosleep (Belirli bir süre uyur)",
    [36] = "getitimer (Zamanlayıcıyı alır)",
    [37] = "alarm (Alarm ayarlar)",
    [38] = "setitimer (Zamanlayıcı ayarlar)",
    [39] = "getpid (Sürecin kimliğini döner)",
    [40] = "sendfile (Dosya içeriğini bir başka dosyaya hızlıca kopyalar)",
    [41] = "socket (Yeni bir soket oluşturur)",
    [42] = "connect (Bir soketi uzak bir adrese bağlar)",
    [43] = "accept (Bir bağlantı isteğini kabul eder)",
    [44] = "sendto (Bir mesajı bir soket üzerinden gönderir)",
    [45] = "recvfrom (Bir soketten mesaj alır)",
    [46] = "sendmsg (Soket üzerinden mesaj gönderir)",
    [47] = "recvmsg (Soketten mesaj alır)",
    [48] = "shutdown (Bir soketi kapatır)",
    [49] = "bind (Soketi bir adrese bağlar)",
    [50] = "listen (Bağlantı isteklerini dinler)",
    [51] = "getsockname (Bir soketin yerel adresini alır)",
    [52] = "getpeername (Bağlı bir soketin uzak adresini alır)",
    [53] = "socketpair (Bağlantılı bir soket çifti oluşturur)",
    [54] = "setsockopt (Soket seçeneklerini ayarlar)",
    [55] = "getsockopt (Soket seçeneklerini alır)",
    [56] = "clone (Yeni bir işlem veya iş parçacığı oluşturur)",
    [57] = "fork (Yeni bir çocuk süreci başlatır)",
    [58] = "vfork (Yeni bir süreç oluşturur, ancak ebeveyn süreci bekler)",
    [59] = "execve (Yeni bir program başlatır)",
    [60] = "exit (Bir süreçten çıkar)",
    [61] = "wait4 (Bir çocuk sürecin bitmesini bekler)",
    [62] = "kill (Bir sürece sinyal gönderir)",
    [63] = "uname (Sistem hakkında bilgi alır)",
    [257] = "openat (Belirli bir dizinden dosya açar)",
    [262] = "newfstatat (Dosya durumu sorgular)",
    [231] = "exit (Bir işlemi sonlandırır)"
};


// Sistem çağrısını ekrana yazdır
printf("Sistem çağrısı: %s (%ld)\n",
       syscall_names[orig_rax] ? syscall_names[orig_rax] : "Bilinmeyen",
       orig_rax);

       // üst sonra ekledim 
            //printf("Sistem çağrısı: %ld\n", orig_rax);

            // Sistem çağrısından sonra devam et
            ptrace(PTRACE_SYSCALL, child, NULL, NULL);
        }
    }
    return 0;
}

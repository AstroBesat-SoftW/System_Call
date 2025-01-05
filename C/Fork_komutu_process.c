#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
// create process işlemi 
int main() {
    pid_t pid = fork(); // Yeni bir süreç oluşturur

    if (pid == 0) {
        // Child process
        char *args[] = {"/bin/ls", "-l", NULL}; // `ls -l` komutunu çalıştırır
        execve("/bin/ls", args, NULL); // Yeni program başlatılır
    } else if (pid > 0) {
        // Parent process
        printf("Parent process: PID = %d, Child PID = %d\n", getpid(), pid);
    } else {
        // Fork hatası
        perror("Fork failed");
    }
    return 0;
}

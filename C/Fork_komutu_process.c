#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
// create process işlemi 
int main() {
    pid_t pid = fork(); // Yeni bir süreç oluşturur

     if (pid > 0) {
        // ebeveyn  process
        printf("Anne process: PID = %d, Cocuk PID = %d\n", getpid(), pid);
    } else {
        // Fork hatası
        
    }
    return 0;
}

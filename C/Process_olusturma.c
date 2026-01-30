#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
// linux için ola kısmı
int main() {
    pid_t pid = fork(); 

    if (pid == 0) {
      
        char *args[] = {"/bin/ls", "-l", NULL}; 
        execve("/bin/ls", args, NULL); 
    } else if (pid > 0) {
        
        printf("Ebeveyn process: PID = %d, Çocuk PID = %d\n", getpid(), pid);
    } else {
        
        perror("Fork hatası");
    }
    return 0;
}

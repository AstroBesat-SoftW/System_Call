#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

// Sayaç fonksiyonu
void* timer_function(void* arg) {
    for (int i = 1; i <= 10; i++) {
        sleep(1);  // 1 saniye bekle
        printf("Sayaç: %d saniye\n", i);
    }
    printf("10 saniye oldu!\n");
    return NULL;
}

// fork işlemi
void* fork_function(void* arg) {
    for (int i = 0; i < 5; i++) {
        sleep(2);  // 2 saniye bekle
        pid_t pid = fork(); // Yeni bir süreç oluşturur

     if (pid > 0) {
        // ebeveyn  process
        printf("Anne process: PID = %d, Cocuk PID = %d\n", getpid(), pid);
    } 
    }
    return NULL;
}

int main() {
    pthread_t timer_thread, fork_thread;

    // Sayaç thread'ini başlat
    pthread_create(&timer_thread, NULL, timer_function, NULL);

    // Merhaba Dünya thread'ini başlat
    pthread_create(&fork_thread, NULL, fork_function, NULL);

    // Thread'lerin tamamlanmasını bekle
    pthread_join(timer_thread, NULL);
    pthread_join(fork_thread, NULL);

    printf("Tum islemler tamamlandi.\n");
    return 0;
}

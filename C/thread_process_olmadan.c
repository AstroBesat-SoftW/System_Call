#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Sayaç fonksiyonu
void timer_function() {
    for (int i = 1; i <= 10; i++) {
        sleep(1);  // 1 saniye bekle
        printf("Sayaç: %d saniye\n", i);
    }
    printf("10 saniye oldu!\n");
}

// fork işlemi
void fork_function() {
    for (int i = 0; i < 5; i++) {
        sleep(2);  // 2 saniye bekle
        pid_t pid = fork(); // Yeni bir süreç oluşturur

     if (pid > 0) {
        // ebeveyn  process
        printf("Anne process: PID = %d, Cocuk PID = %d\n", getpid(), pid);
    } 
    }
}

int main() {
    // Sayaç işlemini başlat
    timer_function();

    // Merhaba Dünya işlemini başlat
    fork_function();

    printf("Tum islemler tamamlandi.\n");
    return 0;
}

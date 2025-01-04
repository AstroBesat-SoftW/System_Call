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

// Merhaba Dünya işlemi
void* hello_world_function(void* arg) {
    for (int i = 0; i < 5; i++) {
        sleep(2);  // 2 saniye bekle
        printf("Merhaba Dünya! %d. kez\n", i + 1);
    }
    return NULL;
}

int main() {
    pthread_t timer_thread, hello_thread;

    // Sayaç thread'ini başlat
    pthread_create(&timer_thread, NULL, timer_function, NULL);

    // Merhaba Dünya thread'ini başlat
    pthread_create(&hello_thread, NULL, hello_world_function, NULL);

    // Thread'lerin tamamlanmasını bekle
    pthread_join(timer_thread, NULL);
    pthread_join(hello_thread, NULL);

    printf("Tum islemler tamamlandi.\n");
    return 0;
}

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

// Merhaba Dünya işlemi
void hello_world_function() {
    for (int i = 0; i < 5; i++) {
        sleep(2);  // 2 saniye bekle
        printf("Merhaba Dünya! %d. kez\n", i + 1);
    }
}

int main() {
    // Sayaç işlemini başlat
    timer_function();

    // Merhaba Dünya işlemini başlat
    hello_world_function();

    printf("Tum islemler tamamlandi.\n");
    return 0;
}

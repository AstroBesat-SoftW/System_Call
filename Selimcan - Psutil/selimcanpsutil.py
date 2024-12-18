import psutil
import time

def sistem_cagrilari_izle():
    print("===== SİSTEM KAYNAKLARI =====")

    # CPU Kullanımı
    print(f"CPU Kullanımı: {psutil.cpu_percent(interval=1)}%")

    # Bellek Kullanımı
    bellek = psutil.virtual_memory()
    print(f"Toplam Bellek: {bellek.total / (1024**3):.2f} GB")
    print(f"Kullanılan Bellek: {bellek.used / (1024**3):.2f} GB")
    print(f"Boş Bellek: {bellek.available / (1024**3):.2f} GB")

    # Disk Kullanımı
    disk = psutil.disk_usage('/')
    print(f"Toplam Disk: {disk.total / (1024**3):.2f} GB")
    print(f"Kullanılan Disk: {disk.used / (1024**3):.2f} GB")
    print(f"Boş Disk: {disk.free / (1024**3):.2f} GB")

    # Ağ Kullanımı
    net_io = psutil.net_io_counters()
    print(f"Gönderilen Veri: {net_io.bytes_sent / (1024**2):.2f} MB")
    print(f"Alınan Veri: {net_io.bytes_recv / (1024**2):.2f} MB")

    # Çalışan Süreçler - İki Aşamalı CPU Kullanımı Ölçümü
    print("\nÇalışan Süreçler (PID, İsim, CPU Kullanımı):")

    # İlk ölçüm: Başlatma için
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    time.sleep(1)  # 1 saniye bekle

    # İkinci ölçüm: Gerçek CPU yüzdesini ölç
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            cpu_percent = proc.cpu_percent(interval=0)
            if cpu_percent > 0:  # Sadece CPU kullanımı olan süreçleri göster
                print(f"PID: {proc.info['pid']}, Ad: {proc.info['name']}, CPU: {cpu_percent}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Hata alan süreçleri atla

if __name__ == "__main__":
    sistem_cagrilari_izle()


from kutuphaneler import *

def log_system_stats():
    """Sistem bilgilerini log dosyasına yazar ve arayüzde gösterir."""
    data = {
        "çekirdek_bilgisi": get_kernel_info(),
        "bellek_bilgisi": get_memory_info(),
        "cpu_bilgisi": get_cpu_info(),
        "disk_bilgisi": get_disk_info(),
        "ağ_bilgisi": get_network_info(),
        "işlem_bilgisi": get_process_info(),
        "sistem_çalışma_süresi": get_system_uptime(),
       
        "disk_io_bilgisi": get_disk_io_counters(),
        "ağ_io_bilgisi": get_net_io_counters(),
    }

    result = "\n".join([

        # Çekirdek Bilgileri
        f"1. Çekirdek Bilgileri:\n"
        f"   - Çekirdek Sürümü: {data['çekirdek_bilgisi']['çekirdek_sürümü']}\n"
        f"   - Sistem Adı: {data['çekirdek_bilgisi']['sistem_adı']}\n"
        f"   - Düğüm Adı: {data['çekirdek_bilgisi']['düğüm_adı']}\n"
        f"   - Makine Türü: {data['çekirdek_bilgisi']['makine_türü']}\n\n",

        # Bellek Bilgileri
        f"2. Bellek Bilgileri:\n"
        f"   - Toplam Bellek: {data['bellek_bilgisi']['toplam_bellek']:.2f} GB\n"
        f"   - Mevcut Bellek: {data['bellek_bilgisi']['mevcut_bellek']:.2f} GB\n"
        f"   - Kullanılan Bellek: {data['bellek_bilgisi']['kullanılan_bellek']:.2f} GB\n"
        f"   - Bellek Kullanım Oranı: {data['bellek_bilgisi']['bellek_kullanım_oranı']}%\n\n",

        # CPU Bilgileri
        f"3. CPU Bilgileri:\n"
        f"   - Fiziksel Çekirdek Sayısı: {data['cpu_bilgisi']['fiziksel_çekirdek_sayısı']}\n"
        f"   - Toplam Çekirdek Sayısı: {data['cpu_bilgisi']['toplam_çekirdek_sayısı']}\n"
        f"   - İşlemci Hızı: {data['cpu_bilgisi']['işlemci_hızı']} MHz\n"
        f"   - Toplam CPU Kullanımı: {data['cpu_bilgisi']['toplam_cpu_kullanımı']}%\n"
        + "\n".join([f"     Çekirdek {idx + 1}: {usage}%\n" for idx, usage in enumerate(data['cpu_bilgisi']['çekirdek_başına_cpu_kullanımı'])]) +
        "\n",

        # Disk Bilgileri
        f"4. Disk Bilgileri:\n"
        + "\n".join([f"   - {mount}:\n"
                    f"     - Toplam Alan: {disk['toplam_disk_alani']:.2f} GB\n"
                    f"     - Kullanılan Alan: {disk['kullanilan_disk_alani']:.2f} GB\n"
                    f"     - Boş Alan: {disk['boş_disk_alani']:.2f} GB\n"
                    f"     - Kullanım Oranı: {disk['disk_kullanım_oranı']}%\n\n"
                    for mount, disk in data['disk_bilgisi'].items()]),

        # Ağ Bilgileri
        f"5. Ağ Bilgileri:\n"
        f"   - Gönderilen Veri: {data['ağ_bilgisi']['gönderilen_veri']} MB\n"
        f"   - Alınan Veri: {data['ağ_bilgisi']['alınan_veri']} MB\n\n",

        # İşlem Bilgileri
        f"6. İşlem Bilgileri:\n"
+ "\n".join([f"   - PID: {process['pid']} | İsim: {process['isim']} | "
             f"CPU Kullanımı: {process['cpu_kullanımı']}% | Bellek Kullanımı: {process['bellek_kullanımı']:.2f} MB | "
             f"Çalışma Zamanı: {process['çalışma_zamanı']}\n"
             for process in data['işlem_bilgisi']]),

        f"\n",

        # Sistem Çalışma Süresi
        f"7. Sistem Çalışma Süresi: {data['sistem_çalışma_süresi']['sistem_çalışma_süresi']}\n\n",

      
        # Disk I/O Bilgileri
        f"9. Disk I/O Bilgileri:\n"
        f"   - Okunan Sayısı: {data['disk_io_bilgisi']['okuma_sayisi']}\n"
        f"   - Yazma Sayısı: {data['disk_io_bilgisi']['yazma_sayisi']}\n"
        f"   - Okunan Byte: {data['disk_io_bilgisi']['okunan_byte']} byte\n"
        f"   - Yazılan Byte: {data['disk_io_bilgisi']['yazilan_byte']} byte\n\n",

        # Ağ I/O Bilgileri
        f"10. Ağ I/O Bilgileri:\n"
        f"   - Gönderilen Byte: {data['ağ_io_bilgisi']['gönderilen_byte']} byte\n"
        f"   - Alınan Byte: {data['ağ_io_bilgisi']['alınan_byte']} byte\n"
        f"   - Gönderilen Paket: {data['ağ_io_bilgisi']['gönderilen_paket']}\n"
        f"   - Alınan Paket: {data['ağ_io_bilgisi']['alınan_paket']}\n"
        f"   - Hata Giren Paket: {data['ağ_io_bilgisi']['hata_giren']}\n"
        f"   - Hata Çıkan Paket: {data['ağ_io_bilgisi']['hata_çıkan']}\n"
    ])

    # Logging to file
    logging.info(result)

    # GUI Update: Ensure the content_text exists before trying to update
    try:
        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, result)
    except NameError:
        print("GUI content_text widget not found.")

def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    return {
        "toplam_cpu_kullanımı": sum(cpu_usage) / len(cpu_usage),
        "fiziksel_çekirdek_sayısı": psutil.cpu_count(logical=False),
        "toplam_çekirdek_sayısı": psutil.cpu_count(logical=True),
        "işlemci_hızı": psutil.cpu_freq().current,
        "çekirdek_başına_cpu_kullanımı": cpu_usage
    }

def get_kernel_info():
    return {
        "çekirdek_sürümü": platform.release(),
        "sistem_adı": platform.system(),
        "düğüm_adı": platform.node(),
        "makine_türü": platform.machine()
    }




def get_memory_info():
    memory = psutil.virtual_memory()
    return {
        "toplam_bellek": memory.total / (1024.0 ** 3),
        "mevcut_bellek": memory.available / (1024.0 ** 3),
        "kullanılan_bellek": memory.used / (1024.0 ** 3),
        "bellek_kullanım_oranı": memory.percent
    }



def get_disk_info():
    usage = psutil.disk_usage('/')
    return {
        "/": {
            "toplam_disk_alani": usage.total / (1024.0 ** 3),
            "kullanilan_disk_alani": usage.used / (1024.0 ** 3),
            "boş_disk_alani": usage.free / (1024.0 ** 3),
            "disk_kullanım_oranı": usage.percent
        }
    }

def get_network_info():
    net_io = psutil.net_io_counters()
    return {
        "gönderilen_veri": net_io.bytes_sent / (1024.0 ** 2),
        "alınan_veri": net_io.bytes_recv / (1024.0 ** 2)
    }



def get_process_info():
    processes = []
    boot_time = psutil.boot_time()  # Bilgisayarın açılış zamanını al
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process = psutil.Process(proc.info['pid'])

            # CPU kullanımını % olarak almak
            cpu_usage = process.cpu_percent(interval=0.1)

            # Bellek kullanımını MB cinsinden almak
            memory_usage = process.memory_info().rss / (1024 ** 2)  # MB cinsinden

            # Başlangıç zamanını almak
            start_time = process.create_time()

            # Başlangıç zamanını yerel tarih ve saat formatına dönüştürme
            start_time_local = time.localtime(start_time)
            start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", start_time_local)

            processes.append({
                "pid": proc.info['pid'],
                "isim": proc.info['name'],
                "cpu_kullanımı": cpu_usage,
                "bellek_kullanımı": memory_usage,
                "çalışma_zamanı": start_time_str,  # Başlangıç zamanını tarih ve saat formatında yaz
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes


def get_system_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    return {"sistem_çalışma_süresi": uptime_str}



def get_disk_io_counters():
    try:
        io_counters = psutil.disk_io_counters()
        return {
            "okuma_sayisi": io_counters.read_count,
            "yazma_sayisi": io_counters.write_count,
            "okunan_byte": io_counters.read_bytes,
            "yazilan_byte": io_counters.write_bytes
        }
    except AttributeError:
        # Eğer disk IO bilgisi alınamıyorsa varsayılan değerler döndür
        return {
            "okuma_sayisi": 0,
            "yazma_sayisi": 0,
            "okunan_byte": 0,
            "yazilan_byte": 0
        }

def get_net_io_counters():
    try:
        io_counters = psutil.net_io_counters()
        return {
            "gönderilen_byte": io_counters.bytes_sent,
            "alınan_byte": io_counters.bytes_recv,
            "gönderilen_paket": io_counters.packets_sent,
            "alınan_paket": io_counters.packets_recv,
            "hata_giren": io_counters.errin,
            "hata_çıkan": io_counters.errout,
            "paket_düşen": io_counters.dropin,
            "paket_düşen_out": io_counters.dropout
        }
    except AttributeError:
        # Eğer ağ IO bilgisi alınamıyorsa varsayılan değerler döndür
        return {
            "gönderilen_byte": 0,
            "alınan_byte": 0,
            "gönderilen_paket": 0,
            "alınan_paket": 0,
            "hata_giren": 0,
            "hata_çıkan": 0,
            "paket_düşen": 0,
            "paket_düşen_out": 0
        }



#api pid sorgu ve arayüz 
from api_pid_sorgu import *

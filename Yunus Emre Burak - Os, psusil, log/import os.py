import os
import psutil
import time
import logging
from datetime import datetime

def setup_logger(log_file="system_monitor.log"):
    """Log yapılandırmasını ayarlar."""
    logger = logging.getLogger("SystemMonitor")
    logger.setLevel(logging.INFO)

    # Log formatını belirleyelim
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Dosyaya loglama
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Konsola loglama
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Sistem İzleme Başlatıldı")
    return logger

def get_size(bytes):
    """Bayt cinsinden verilen boyutu daha okunabilir bir formata dönüştürür."""
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}B"
        bytes /= 1024

def log_cpu_memory_disk_info(logger):
    """CPU, RAM ve Disk bilgilerini toplar ve loglar."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        logger.info(f"CPU Kullanımı: {cpu_percent:.1f}%")
        logger.info(f"RAM Kullanımı: {mem.percent:.1f}% ({get_size(mem.used)} / {get_size(mem.total)})")
        logger.info(f"Disk Kullanımı: {disk.percent:.1f}% ({get_size(disk.used)} / {get_size(disk.total)})")
    except Exception as e:
        logger.error(f"CPU, RAM veya Disk bilgisini loglarken hata oluştu: {e}")

def log_network_info(logger):
    """Ağ bilgilerini toplar ve loglar."""
    try:
        net = psutil.net_io_counters()
        logger.info(f"Gönderilen Veri: {get_size(net.bytes_sent)}")
        logger.info(f"Alınan Veri: {get_size(net.bytes_recv)}")
    except Exception as e:
        logger.error(f"Ağ bilgilerini loglarken hata oluştu: {e}")

def log_top_processes(logger, top_n=5):
    """En çok CPU ve RAM kullanan işlemleri loglar."""
    try:
        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        sorted_processes = sorted(
            processes,
            key=lambda p: (p.info['cpu_percent'], p.info['memory_percent']),
            reverse=True
        )[:top_n]

        logger.info("En Çok Kaynak Kullanan İşlemler:")
        for proc in sorted_processes:
            try:
                logger.info(f"  PID: {proc.info['pid']}, Ad: {proc.info['name']}, CPU: {proc.info['cpu_percent']:.1f}%, RAM: {proc.info['memory_percent']:.1f}%")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        logger.error(f"İşlem bilgilerini loglarken hata oluştu: {e}")

def monitor_system(interval=10, log_file="system_monitor.log"):
    """Sistemi belirli aralıklarla izler."""
    logger = setup_logger(log_file)
    logger.info(f"İzleme Aralığı: {interval} saniye")

    try:
        while True:
            logger.info("--- Sistem Bilgileri ---")
            log_cpu_memory_disk_info(logger)
            log_network_info(logger)
            log_top_processes(logger, top_n=10)
            logger.info("------------------------")
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Sistem İzleme Durduruldu")
        print("Sistem izleme durduruldu.")
    except Exception as e:
        logger.error(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    monitor_system(interval=10)


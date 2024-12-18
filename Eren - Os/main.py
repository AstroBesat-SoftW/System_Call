import os
from datetime import datetime
import time


def write_log(message, log_dir="logs", log_file="system_monitor.log"):

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"

    with open(log_path, "a") as file:
        file.write(log_message)

    print(log_message.strip())


def get_memory_info():

    vm_stat_output = os.popen("vm_stat").read()
    lines = vm_stat_output.splitlines()
    page_size = int(lines[0].split("of")[1].strip().split(" ")[0])  # Sayfa boyutu (byte)

    mem_free = int(lines[1].split(":")[1].strip().replace(".", "")) * page_size
    mem_active = int(lines[2].split(":")[1].strip().replace(".", "")) * page_size
    mem_inactive = int(lines[3].split(":")[1].strip().replace(".", "")) * page_size
    mem_wired = int(lines[4].split(":")[1].strip().replace(".", "")) * page_size

    total_memory = (mem_free + mem_active + mem_inactive + mem_wired) / (1024 ** 2)
    return {
        "free_memory_mb": mem_free / (1024 ** 2),
        "active_memory_mb": mem_active / (1024 ** 2),
        "inactive_memory_mb": mem_inactive / (1024 ** 2),
        "wired_memory_mb": mem_wired / (1024 ** 2),
        "total_memory_mb": total_memory
    }

def get_cpu_usage():
    """CPU kullanım oranını alır."""
    cpu_usage_output = os.popen("top -l 1 | grep 'CPU usage'").read().strip()
    if cpu_usage_output:
        try:


            usage_parts = cpu_usage_output.split(",")


            cpu_user = float(usage_parts[0].split()[-2].strip('%'))
            cpu_system = float(usage_parts[1].split()[-2].strip('%'))
            cpu_idle = float(usage_parts[2].split()[-2].strip('%'))
            return {"user": cpu_user, "system": cpu_system, "idle": cpu_idle}
        except (IndexError, ValueError):

            write_log("CPU kullanım bilgisi ayrıştırılamadı.")
            return {"user": 0.0, "system": 0.0, "idle": 100.0}
    return {"user": 0.0, "system": 0.0, "idle": 100.0}


def get_disk_usage():

    disk_usage_output = os.popen("df -h /").read().splitlines()[1]
    parts = disk_usage_output.split()
    total = parts[1]
    used = parts[2]
    available = parts[3]
    percent_used = parts[4]
    return {"total": total, "used": used, "available": available, "percent_used": percent_used}


def get_network_stats():

    netstat_output = os.popen("netstat -ib").read().splitlines()
    total_in = 0
    total_out = 0

    for line in netstat_output[1:]:
        parts = line.split()
        if len(parts) > 9:
            total_in += int(parts[6])  # Gelen baytlar
            total_out += int(parts[9])  # Giden baytlar

    return {"bytes_in": total_in, "bytes_out": total_out}


def monitor_system(interval=5, duration=60):

    start_time = time.time()
    while time.time() - start_time < duration:

        memory_info = get_memory_info()
        write_log(f"Memory: {memory_info}")


        cpu_info = get_cpu_usage()
        write_log(f"CPU Usage: User {cpu_info['user']}%, System {cpu_info['system']}%, Idle {cpu_info['idle']}%")


        disk_info = get_disk_usage()
        write_log(f"Disk: Total {disk_info['total']}, Used {disk_info['used']}, "
                  f"Available {disk_info['available']}, Percent Used {disk_info['percent_used']}")


        network_info = get_network_stats()
        write_log(f"Network: Incoming {network_info['bytes_in']} bytes, Outgoing {network_info['bytes_out']} bytes")


        time.sleep(interval)


if __name__ == "__main__":
    print("Sistem izlemeye başladı. Çıkmak için Ctrl+C yapabilirsiniz.")
    monitor_system(interval=5, duration=60)

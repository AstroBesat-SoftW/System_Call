import subprocess
import datetime
import os

def system_info_log(log_file="system_log.txt"):
    log_path = os.path.abspath(log_file)

    try:
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(f"\nSistem Bilgisi Logu - {datetime.datetime.now()}\n")
            log.write("="*50 + "\n\n")

            def run_command(description, command):
                log.write(f"{description}:\n")
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    stdout=log, stderr=subprocess.PIPE, text=True
                )
                if result.returncode != 0:
                    log.write(f"Hata: {result.stderr}\n")
                log.write("\n")

            run_command("CPU Kullanımı", "Get-CimInstance Win32_Processor | Select-Object -Property LoadPercentage")
            run_command("Fiziksel Bellek Bilgisi", "Get-CimInstance Win32_OperatingSystem | Select-Object -Property FreePhysicalMemory, TotalVisibleMemorySize")
            run_command("Çalışan İşlemler", "Get-Process | Format-Table -Property Id, ProcessName, CPU -AutoSize")
            run_command("Disk Kullanımı", "Get-CimInstance Win32_LogicalDisk | Select-Object DeviceID, FreeSpace, Size")
            run_command("Ağ Bağdaştırıcıları", "Get-NetAdapter | Format-List Name, Status, MacAddress")
            run_command("Sistem Çalışma Süresi", "Get-CimInstance Win32_OperatingSystem | Select-Object LastBootUpTime")

        print(f"Sistem bilgileri kaydedildi: {log_path}")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    system_info_log()

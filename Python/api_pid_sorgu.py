from kutuphaneler import *
from api_key import *
from log_sistem_verileri import *


def get_pid_details():
    """Belirtilen PID'nin detaylarını alır, analiz eder ve arayüzde gösterir."""
    pid = simpledialog.askinteger("PID Ara", "PID numarasını girin:")
    if pid is None:
        return

    try:
        proc = psutil.Process(pid)
        details = f"--- Detaylı PID Bilgisi ---\n"
        details += f"PID: {pid}\n"
        details += f"Adı: {proc.name()}\n"
        details += f"Kullanıcı: {proc.username()}\n"
        details += f"CPU Kullanımı: {proc.cpu_percent(interval=1.0)}%\n"
        details += f"Bellek Kullanımı: {proc.memory_info().rss / (1024 ** 2):.2f} MB\n"
        details += f"Başlangıç Zamanı: {datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')}\n"

        # ChatGPT analizi
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Sistem süreçlerini analiz eden bir asistansın. Gelen bilgileri Türkçe analiz et. (ekstra olarak sürecin 'adı:' var işte mesela 4 pıd system diyelim adı onun hakkında hakkında detaylı bilgi ver kullanım yerlerine örnekler ver)"},
                {"role": "user", "content": details}
            ]
        )
        analysis = response['choices'][0]['message']['content']
        details += f"\n--- Analiz ---\n{analysis}\n"

        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, details)

        save = messagebox.askyesno("Kaydet", "Sonuç kaydedilsin mi?")
        if save:
            with open(f"Kayitlar/{pid}.txt", "w", encoding="utf-8") as file:
                file.write(details)
            messagebox.showinfo("Başarılı", f"Sonuç {pid}.txt olarak kaydedildi.")

    except psutil.NoSuchProcess:
        messagebox.showerror("Hata", f"PID {pid} mevcut değil.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

from arayuz import *


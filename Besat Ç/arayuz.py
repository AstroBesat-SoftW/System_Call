from kutuphaneler import *
from log_sistem_verileri import *
from api_key import *

from api_pid_sorgu import *


def exit_app():
    if messagebox.askyesno("Çıkış", "Uygulamadan çıkmak istediğinize emin misiniz?"):
        root.destroy()

def save_as(format):
    """Metni belirtilen formatta kaydeder."""
    file_name = simpledialog.askstring("Dosya Adı", "Dosya adını girin:")
    if not file_name:
        return

    content = content_text.get("1.0", tk.END).strip()  # Boşlukları ve son satırı kaldır
    try:
        if format == "txt":
            with open(f"Kayitlar/{file_name}.txt", "w", encoding="utf-8") as file:
                file.write(content)
        elif format == "pdf":
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            # Türkçe karakter desteği için bir font ekle
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=12)
            for line in content.splitlines():
                pdf.multi_cell(0, 10, txt=line)  # Satır taşmalarını düzgün işler
            pdf.output(f"Kayitlar/{file_name}.pdf", "F")
        messagebox.showinfo("Başarılı", f"Dosya {file_name}.{format} olarak kaydedildi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Dosya kaydedilemedi: {e}")

def show_purpose():
    """Uygulamanın amacını gösterir."""
    purpose = (
        "Bu uygulama, sistem çağrılarını izlemek ve analiz etmek için tasarlanmıştır.\n"
        "Ayrıca, belirli işlemler hakkında detaylı bilgi sunar ve yapay zeka destekli analiz yapar. \n\nGeliştirici - Besat Arif Çıngar"
    )
    messagebox.showinfo("Amacımız", purpose)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Sistem Çağrılarını İzleme")
root.attributes('-fullscreen', True)  # Tam ekran yap


# Üstteki menü çubuğu
menu_bar = Menu(root)

menu = Menu(menu_bar, tearoff=0)
menu.add_command(label="TXT olarak kaydet", command=lambda: save_as("txt"))
menu.add_command(label="PDF olarak kaydet", command=lambda: save_as("pdf"))
menu_bar.add_cascade(label="Kaydet", menu=menu)

purpose_menu = Menu(menu_bar, tearoff=0)
purpose_menu.add_command(label="Amacımız", command=show_purpose)
menu_bar.add_cascade(label="Amacımız", menu=purpose_menu)

exit_menu = Menu(menu_bar, tearoff=0)
exit_menu.add_command(label="Çıkış", command=exit_app)
menu_bar.add_cascade(label="Çıkış", menu=exit_menu)

root.config(menu=menu_bar)



# Sol panel
left_frame = tk.Frame(root, bg="#404040", width=200)
left_frame.grid(row=0, column=0, sticky="ns")

btn_log = ttk.Button(left_frame, text="Sistem Çağrılarını İncele", command=log_system_stats)
btn_log.pack(pady=10, padx=10, fill="x")

btn_pid = ttk.Button(left_frame, text="PID Ara", command=get_pid_details)
btn_pid.pack(pady=10, padx=10, fill="x")

# Sağ panel
content_frame = tk.Frame(root, bg="white")
content_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
content_text = tk.Text(content_frame, wrap="word")
content_text.pack(expand=True, fill="both")

# Grid yapılandırması
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

import os
import time


def log_system_call(call_type, details):
    with open("System_calls.log", "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {call_type}: {details}\n")


def list_directory():
    files = os.listdir(".")
    log_system_call("listdir", f"Listelenen dosyalar: {files}")
    return files


def create_directory(dir_name):
    os.mkdir(dir_name)
    log_system_call("mkdir", f"{dir_name} dizini oluşturuldu.")


def remove_directory(dir_name):
    os.rmdir(dir_name)
    log_system_call("rmdir", f"{dir_name} dizini silindi.")


def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
            log_system_call("read", f"{file_name} dosyası okundu.")
            return content
    except FileNotFoundError:
        log_system_call("read_error", f"{file_name} dosyası bulunamadı.")
        print("Hata: Dosya bulunamadı.")
        return None


def write_file(file_name, content):
    with open(file_name, "w") as file:
        file.write(content)
        log_system_call("write", f"{file_name} dosyasına yazıldı: {content}")


def view_logs():
    try:
        with open("System_calls.log", "r") as log_file:
            print("Log dosyası içeriği:")
            print(log_file.read())
    except FileNotFoundError:
        print("Log dosyası henüz oluşturulmamış.")


def main():
    print("Sistem çağrılarını izleyen uygulama")
    print("1: Dizindeki dosyaları listele")
    print("2: Yeni bir dizin oluştur")
    print("3: Bir dizini sil")
    print("4: Bir dosyayı oku")
    print("5: Bir dosyaya yaz")
    print("6: Log dosyasını görüntüle")
    print("7: Çıkış yap")

    while True:
        choice = input("\nSeçiminizi yapınız (1-7): ")

        if choice == "1":
            print("Mevcut dosyalar:", list_directory())

        elif choice == "2":
            dir_name = input("Oluşturulacak dizinin adı: ")
            create_directory(dir_name)

        elif choice == "3":
            dir_name = input("Silinecek dizin adı: ")
            remove_directory(dir_name)

        elif choice == "4":
            file_name = input("Okunacak dosya adı: ")
            content = read_file(file_name)
            if content:
                print("Dosya içeriği:", content)

        elif choice == "5":
            file_name = input("Dosya adı: ")
            content = input("Yazılacak içerik: ")
            write_file(file_name, content)

        elif choice == "6":
            view_logs()

        elif choice == "7":
            print("Uygulama sonlandırılıyor...")
            break

        else:
            print("Geçersiz seçim yaptınız. Lütfen tekrar deneyiniz.")


if __name__ == "__main__":
    main()

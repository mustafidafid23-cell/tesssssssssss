# GENSHIN DPS TRACKER
import data
from data import akun
from func import *
import admin_menu
import user_menu

# AUTENTIKASI
def registrasi():
    bersihkan_layar()
    cetak_header("          REGISTRASI AKUN", garis_40)

    username_baru = input("Buat username: ").strip()
    password_baru = input("Buat password: ").strip()
    try:
        validasi_akun_baru(username_baru, password_baru)
    except ValueError as e:
        print(e)
    else:
        akun[username_baru] = {"password": password_baru, "role": "User"}
        print("Registrasi berhasil!")
        print("Silakan login menggunakan akun baru.")
    finally:
        jeda()

def login():   
    batas_percobaan = 3
    while batas_percobaan > 0:
        bersihkan_layar()
        cetak_header("             LOGIN", garis_40)

        if batas_percobaan < 3:
            print(f"[!] Peringatan: sisa percobaan login tinggal {batas_percobaan} kali. ")

        username_input = input("Username: ").strip()
        password_input = input("Password: ").strip()

        try:
            if username_input not in akun or akun[username_input]["password"] != password_input:
                raise ValueError("Username atau Password salah")

        except ValueError as e:
            batas_percobaan -= 1
            print (f"\n--> Error: {e}")

            if batas_percobaan == 0:
                print("Batas Percobaan Habis. Anda Dikembalikan Ke Menu Awal. ")
                jeda(enter_kembali_rapat)
                return None
            else:
                jeda("Tekan Enter Untuk Mencoba lagi...")
        else:
            role_akun = akun[username_input]["role"]
            print("\nLogin berhasil!")
            print("Selamat datang,", username_input)
            print("Role:", role_akun)
            jeda("\nTekan Enter untuk masuk ke menu...")
            return username_input, role_akun

# PROGRAM UTAMA (Multiuser: Admin & User)
def jalankan_program():
    while True:
        bersihkan_layar()
        cetak_header("       GENSHIN DPS TRACKER", garis_40)
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")
        pilihan_awal = input("Pilih menu: ").strip()

        if pilihan_awal == "3":
            print("\nTerima kasih telah menggunakan DPS Tracker!")
            break
        if pilihan_awal == "2":
            registrasi()
            continue
        if pilihan_awal != "1":
            print("Pilihan tidak valid.")
            jeda(enter_kembali_rapat)
            continue

        hasil_login = login()
        if hasil_login is None:
            continue
        
        username_aktif, role_aktif = hasil_login
        if role_aktif == "Admin":
            admin_menu.menu_admin()
        elif role_aktif == "User":
            user_menu.menu_user(username_aktif)

if __name__ == "__main__":
    try:
        jalankan_program()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram dihentikan.")
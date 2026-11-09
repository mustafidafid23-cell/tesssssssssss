import os
from datetime import datetime
from prettytable import PrettyTable, ALL
import data
from data import akun, genshin_characters, preset, dummy, team, build, riwayat, id_tes_berikutnya

# VARIABEL GLOBAL (dipakai oleh banyak fungsi)
clear_cmd = "cls" if os.name == "nt" else "clear"
garis_40 = "=" * 40
garis_45 = "=" * 45
garis_55 = "=" * 55
strip_30 = "-" * 30
strip_40 = "-" * 40
strip_45 = "-" * 45
strip_55 = "-" * 55
enter_kembali = "\nTekan Enter untuk kembali..."
enter_kembali_rapat = "Tekan Enter untuk kembali..."

def waktu_tes():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def buat_tabel_riwayat(admin_mode=False):
    tabel = PrettyTable()
    # Jika admin, tampilkan kolom Pemilik (Username)
    if admin_mode:
        tabel.field_names = ["ID Tes", "Waktu", "Pemilik", "Tim", "Build", "Preset", "Target", "Hasil DPS"]
    else:
        tabel.field_names = ["ID Tes", "Waktu", "Tim", "Build", "Preset", "Target", "Hasil DPS"]
    tabel.align = "L"
    tabel.align["ID Tes"] = "c"
    tabel.align["Hasil DPS"] = "r"
    tabel.hrules = ALL
    return tabel

def buat_tabel_preset():
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Nama Preset", "Deskripsi"]
    tabel.align["ID"] = "C"
    tabel.align["Nama Preset"] = "L"
    tabel.align["Deskripsi"] = "L"
    tabel.max_width["Nama Preset"] = 20
    tabel.max_width["Deskripsi"] = 45
    tabel.hrules = ALL
    return tabel

def buat_tabel_dummy():
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Nama Target", "Kategori", "Deskripsi"]
    tabel.align["ID"] = "c"
    tabel.align["Nama Target"] = "L"
    tabel.align["Kategori"] = "c"
    tabel.align["Deskripsi"] = "L"
    tabel.max_width["Deskripsi"] = 40
    tabel.hrules = ALL
    return tabel

# FUNGSI REKURSIF 
def format_ribuan(angka):
    # Base case
    if angka < 1000:
        return str(angka)
    # Recursive case
    return format_ribuan(angka // 1000) + "." + str(angka % 1000).zfill(3)

def cari_nama_rekursif(daftar_nama, nama, indeks=0):
    # Base case 1: sudah sampai akhir list
    if indeks >= len(daftar_nama):
        return None
    # Base case 2: ditemukan
    if daftar_nama[indeks].lower() == nama.lower():
        return daftar_nama[indeks]
    # Recursive case
    return cari_nama_rekursif(daftar_nama, nama, indeks + 1)

# FUNGSI DENGAN PARAMETER
def cari_karakter(nama):
    try:
        return cari_nama_rekursif(list(genshin_characters), nama)
    except RecursionError:
        # Cadangan jika daftar karakter terlalu panjang untuk rekursi
        return next((item for item in genshin_characters if item.lower() == nama.lower()), None)

def baca_id(teks, label):
    if not teks.isdigit():
        raise ValueError(f"{label} harus berupa angka.")
    return int(teks)

def pilih_id(data, prompt, label, pesan_tidak_ditemukan):
    id_target = baca_id(input(prompt).strip(), label)
    if id_target not in data:
        raise ValueError(pesan_tidak_ditemukan)
    return id_target

def pilih_dari_daftar(daftar, prompt, label, pesan_tidak_ditemukan):
    id_target = baca_id(input(prompt).strip(), label)
    data_dipilih = next((item for item in daftar if item["id"] == id_target), None)
    if data_dipilih is None:
        raise ValueError(pesan_tidak_ditemukan)
    return data_dipilih

def tentukan_elemen(nama_valid):
    elemen = genshin_characters[nama_valid]
    if not isinstance(elemen, set):
        return elemen
    print("Pilihan elemen Traveler:")
    for pilihan_elemen in sorted(elemen):
        print("-", pilihan_elemen)
    elemen_pilihan = input("Pilih elemen Traveler: ").strip()
    elemen_valid = cari_nama_rekursif(sorted(elemen), elemen_pilihan)
    if elemen_valid is None:
        raise ValueError("Elemen Traveler tidak valid.")
    return elemen_valid

def validasi_akun_baru(username_baru, password_baru):
    if username_baru == "" or password_baru.strip() == "":
        raise ValueError("Username dan password tidak boleh kosong.")
    if username_baru in akun:
        raise ValueError("Username sudah digunakan.")

def validasi_anggota_baru(daftar_baru):
    karakter_valid = []
    elemen_baru = {}
    for nama in daftar_baru:
        nama_valid = cari_karakter(nama)
        if nama_valid is None:
            raise ValueError("Karakter tidak ditemukan: " + nama)
        if nama_valid in karakter_valid:
            raise ValueError("Karakter duplikat: " + nama_valid)
        elemen_baru[nama_valid] = tentukan_elemen(nama_valid)
        karakter_valid.append(nama_valid)
    return karakter_valid, elemen_baru

def tim_dipakai(id_tim):
    return (
        any(data_build["id_team"] == id_tim for data_build in build)
        or any(data_tes["id_team"] == id_tim for data_tes in riwayat)
    )

def ambil_tim_saya(username_pemilik):
    return [data_tim for data_tim in team if data_tim["username"] == username_pemilik]

def ambil_build_saya(username_pemilik):
    return [data_build for data_build in build if data_build["username"] == username_pemilik]

def ambil_riwayat_saya(username_pemilik):
    return [data_tes for data_tes in riwayat if data_tes["username"] == username_pemilik]

def konfirmasi_ya(pertanyaan):
    return input(pertanyaan).strip().lower() == "ya"

def kumpulkan_anggota_tim():
    karakter_tim = []
    elemen_tim = {}

    while len(karakter_tim) < 4:
        print("\nAnggota saat ini:", karakter_tim)
        print("Ketik 'selesai' untuk menyimpan tim.")
        pilihan_karakter = input("Masukkan nama karakter: ").strip()
        if pilihan_karakter.lower() == "selesai":
            break

        try:
            nama_valid = cari_karakter(pilihan_karakter)
            if nama_valid is None:
                raise ValueError("Karakter tidak ditemukan.")
            if nama_valid in karakter_tim:
                raise ValueError("Karakter tersebut sudah ada di tim.")
            elemen = tentukan_elemen(nama_valid)
        except ValueError as e:
            print(e)
        else:
            elemen_tim[nama_valid] = elemen
            karakter_tim.append(nama_valid)
            print("Karakter berhasil ditambahkan.")

    return karakter_tim, elemen_tim

def kumpulkan_build_karakter(tim_dipilih):
    karakter_build = []
    print("\nMasukkan build setiap karakter dalam tim.")
    print("Isi senjata dan artefak untuk karakter tim.\n")

    for nomor, nama_karakter in enumerate(tim_dipilih["karakter"], start=1):
        print(f"\nKarakter {nomor}: {nama_karakter}")
        elemen = tim_dipilih["elemen"][nama_karakter]
        senjata = input("Nama senjata: ").strip()
        artefak = input("Nama artefak: ").strip()

        try:
            if not senjata or not artefak:
                raise ValueError("Senjata dan artefak tidak boleh kosong.")
        except ValueError as e:
            print(e)
            return []
        else:
            karakter_build.append({
                "karakter": nama_karakter,
                "elemen": elemen,
                "senjata": senjata,
                "artefak": artefak
            })
    return karakter_build

# FUNGSI TANPA PARAMETER (mengembalikan nilai)
def minta_pilihan():
    return input("Pilih menu: ").strip()

def buat_id_tes():
    global id_tes_berikutnya
    id_sekarang = id_tes_berikutnya
    id_tes_berikutnya += 1
    return id_sekarang

def hitung_total_karakter():
    return len(genshin_characters)

# PROSEDUR (tanpa return) - TAMPILAN UMUM
def bersihkan_layar():
    os.system(clear_cmd)

def cetak_header(judul, garis):
    print(garis)
    print(judul)
    print(garis)

def jeda(pesan=enter_kembali):
    input(pesan)

def cetak_karakter_build(nomor, data_karakter, indent_judul="", indent_detail="", lebar_label=7):
    print(f"\n{indent_judul}Karakter {nomor}: {data_karakter['karakter']}")
    print(indent_detail + "Elemen".ljust(lebar_label) + " :", data_karakter["elemen"])
    print(indent_detail + "Senjata".ljust(lebar_label) + " :", data_karakter["senjata"])
    print(indent_detail + "Artefak".ljust(lebar_label) + " :", data_karakter["artefak"])

def cetak_ringkas_karakter(daftar_karakter):
    for nomor, data_karakter in enumerate(daftar_karakter, start=1):
        print(
            f'{nomor}. {data_karakter["karakter"]} | '
            f'Senjata: {data_karakter["senjata"]} | '
            f'Artefak: {data_karakter["artefak"]}'
        )

def tampilkan_pilihan_preset():
    print("\n" + garis_45)
    print("           PILIH PRESET TES")
    print(garis_45)
    for id_item, data_preset in preset.items():
        print(f'\nID Preset : {id_item}')
        print(f'Nama      : {data_preset["nama"]}')
        print(f'Deskripsi : {data_preset["deskripsi"]}')

def tampilkan_pilihan_dummy():
    print("\n" + garis_45)
    print("          PILIH TARGET DUMMY")
    print(garis_45)
    for id_item, data_dummy in dummy.items():
        print(f'\nID Dummy  : {id_item}')
        print(f'Nama      : {data_dummy["nama"]}')
        print(f'Kategori  : {data_dummy["kategori"]}')
        print(f'Deskripsi : {data_dummy["deskripsi"]}')

def daftar_id_nama(data):
    for id_item, data_item in data.items():
        print(id_item, "-", data_item["nama"])
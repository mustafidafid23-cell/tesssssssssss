from data import akun, genshin_characters, preset, dummy, team, build, riwayat
from func import *
import random

# USER - DAFTAR KARAKTER
def lihat_daftar_karakter():
    bersihkan_layar()
    cetak_header("          DAFTAR KARAKTER", garis_40)

    if not genshin_characters:
        print("Belum ada karakter yang tersedia.")
    else:
        tabel = PrettyTable()
        tabel.field_names = ["No", "Jenis Elemen", "Daftar Nama Karakter"]
        tabel.align["No"] = "c"
        tabel.align["Jenis Elemen"] = "L"
        tabel.align["Daftar Nama Karakter"] = "L"
        tabel.max_width["Daftar Nama Karakter"] = 50
        tabel.hrules = ALL

        kelompok_elemen = {}
        for nama_karakter, elemen in genshin_characters.items():
            if isinstance(elemen, set):
                ket_elemen = "Multi-Elemen (" + ", ".join(sorted(elemen)) + ")"
                kelompok_elemen.setdefault(ket_elemen, []).append(nama_karakter)
            else:
                kelompok_elemen.setdefault(elemen, []).append(nama_karakter)

        for nomor, (elemen, daftar_nama) in enumerate(kelompok_elemen.items(), start=1):
            tabel.add_row([nomor, elemen, ", ".join(daftar_nama)])

        print(tabel)
    print("Total Karakter:", hitung_total_karakter())
    jeda()

# USER - KELOLA TIM
def lihat_tim_saya(username_aktif):
    bersihkan_layar()
    cetak_header("               TIM SAYA", garis_40)
    tim_saya = ambil_tim_saya(username_aktif)

    if not tim_saya:
        print("Kamu belum memiliki tim.")
    else:
        for data_tim in tim_saya:
            print("\nID Tim:", data_tim["id"])
            print("Nama Tim:", data_tim["nama_tim"])
            print("Anggota:")
            for nama_karakter in data_tim["karakter"]:
                elemen = data_tim["elemen"].get(nama_karakter, genshin_characters[nama_karakter])
                print("-", nama_karakter, "-", elemen)
            print(strip_40)
    jeda()

def buat_tim(username_aktif):
    bersihkan_layar()
    cetak_header("               BUAT TIM", garis_40)
    nama_tim = input("Masukkan nama tim: ").strip()

    try:
        if nama_tim == "":
            raise ValueError("Nama tim tidak boleh kosong.")
        if any(
            data_tim["username"] == username_aktif and data_tim["nama_tim"].lower() == nama_tim.lower()
            for data_tim in team
        ):
            raise ValueError("Nama tim tersebut sudah di gunakan.")
    except ValueError as e:
        print(e)
        jeda()
        return

    karakter_tim, elemen_tim = kumpulkan_anggota_tim()

    try:
        if len(karakter_tim) == 0:
            raise ValueError("Tim tidak boleh kosong.")
    except ValueError as e:
        print(e)
    else:
        id_terpakai = {data_tim["id"] for data_tim in team}
        id_team_baru = random.randint(1,100000) 
        while id_team_baru in id_terpakai:
            id_team_baru = random.randint(1,100000)
        team.append({
            "id": id_team_baru,
            "username": username_aktif,
            "nama_tim": nama_tim,
            "karakter": karakter_tim,
            "elemen": elemen_tim
        })
        print("\nTim berhasil dibuat dengan ID:", id_team_baru)
    finally:
        jeda()

def ubah_nama_tim(tim_dipilih, username_aktif):
    nama_baru = input("Nama tim baru (Enter untuk tetap): ").strip()
    if nama_baru == "":
        return
    try:
        nama_duplikat = any(
            data_tim["id"] != tim_dipilih["id"]
            and data_tim["username"] == username_aktif
            and data_tim["nama_tim"].lower() == nama_baru.lower()
            for data_tim in team
        )
        if nama_duplikat:
            raise ValueError("Nama tim tersebut sudah kamu gunakan.")
    except ValueError as e:
        print(e)
    else:
        tim_dipilih["nama_tim"] = nama_baru

def ubah_anggota_tim(tim_dipilih):
    print("\nAnggota saat ini:", tim_dipilih["karakter"])
    print("Masukkan karakter baru dipisahkan dengan koma.")
    print("Ketik 'tetap' untuk mempertahankan anggota.")
    input_karakter = input("Anggota baru: ").strip()

    if input_karakter.lower() == "tetap" or input_karakter == "":
        return

    daftar_baru = [nama.strip() for nama in input_karakter.split(",") if nama.strip() != ""]

    try:
        karakter_valid, elemen_baru = validasi_anggota_baru(daftar_baru)
    except ValueError as e:
        print(e)
        print("Perubahan anggota dibatalkan.")
        return
    if len(karakter_valid) == 0:
        print("Perubahan anggota dibatalkan.")
        return

    try:
        if len(karakter_valid) > 4:
            raise ValueError("Tim maksimal terdiri dari 4 karakter.")
        if tim_dipakai(tim_dipilih["id"]):
            raise ValueError(
                "Anggota tim tidak dapat diubah "
                "karena sudah digunakan pada build "
                "atau riwayat tes."
            )
    except ValueError as e:
        print(e)
    else:
        tim_dipilih["karakter"] = karakter_valid
        tim_dipilih["elemen"] = elemen_baru
        print("Anggota tim berhasil diperbarui.")

def ubah_tim(username_aktif):
    bersihkan_layar()
    cetak_header("               UBAH TIM", garis_40)
    tim_saya = ambil_tim_saya(username_aktif)
    if not tim_saya:
        print("Kamu belum memiliki tim.")
        jeda()
        return

    for data_tim in tim_saya:
        print(
            "ID:", data_tim["id"],
            "| Nama:", data_tim["nama_tim"],
            "| Anggota:", ", ".join(data_tim["karakter"])
        )

    try:
        tim_dipilih = pilih_dari_daftar(
            tim_saya, "\nMasukkan ID tim yang ingin diubah: ", "ID tim", "Tim tidak ditemukan."
        )
    except ValueError as e:
        print(e)
        jeda()
        return

    ubah_nama_tim(tim_dipilih, username_aktif)
    ubah_anggota_tim(tim_dipilih)
    print("\nProses perubahan tim selesai.")
    jeda()

def hapus_tim(username_aktif):
    bersihkan_layar()
    cetak_header("              HAPUS TIM", garis_40)
    tim_saya = ambil_tim_saya(username_aktif)
    if not tim_saya:
        print("Kamu belum memiliki tim.")
        jeda()
        return

    for data_tim in tim_saya:
        print("ID:", data_tim["id"], "| Nama:", data_tim["nama_tim"])

    try:
        tim_dipilih = pilih_dari_daftar(
            tim_saya, "\nMasukkan ID tim yang ingin dihapus: ", "ID tim", "Tim tidak ditemukan."
        )
        if tim_dipakai(tim_dipilih["id"]):
            raise ValueError("Tim tidak dapat dihapus karena sudah digunakan pada build atau riwayat tes.")
    except ValueError as e:
        print(e)
    else:
        if konfirmasi_ya("Yakin ingin menghapus tim ini? (ya/tidak): "):
            team.remove(tim_dipilih)
            print("Tim berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    finally:
        jeda()

def kelola_tim(username_aktif):
    while True:
        bersihkan_layar()
        cetak_header("             KELOLA TIM", garis_40)
        print("1. Lihat Tim Saya")
        print("2. Buat Tim")
        print("3. Ubah Tim")
        print("4. Hapus Tim")
        print("5. Kembali")
        pilihan_tim = minta_pilihan()

        if pilihan_tim == "1":
            lihat_tim_saya(username_aktif)
        elif pilihan_tim == "2":
            buat_tim(username_aktif)
        elif pilihan_tim == "3":
            ubah_tim(username_aktif)
        elif pilihan_tim == "4":
            hapus_tim(username_aktif)
        elif pilihan_tim == "5":
            break
        else:
            print("Pilihan tidak valid.")
            jeda("\nTekan Enter untuk mencoba lagi...")

# USER - KELOLA BUILD KARAKTER
def lihat_build_saya(username_aktif):
    bersihkan_layar()
    cetak_header("          DAFTAR KONFIGURASI BUILD", garis_45)
    build_saya = ambil_build_saya(username_aktif)

    if not build_saya:
        print("Kamu belum memiliki konfigurasi build.")
    else:
        for data_build in build_saya:
            print("\nID Build   :", data_build["id"])
            print("Nama Build :", data_build["nama_build"])
            print("Nama Tim   :", data_build["nama_tim"])
            for nomor, data_karakter in enumerate(data_build["karakter_build"], start=1):
                cetak_karakter_build(nomor, data_karakter, indent_judul="  ", indent_detail="  ", lebar_label=8)
            print(strip_45)
    jeda()

def buat_build(username_aktif):
    bersihkan_layar()
    tim_saya = ambil_tim_saya(username_aktif)
    if not tim_saya:
        print("Kamu belum memiliki tim.")
        jeda(enter_kembali_rapat)
        return

    cetak_header("          PILIH TIM", garis_45)
    for data_tim in tim_saya:
        print(f'ID: {data_tim["id"]} | Nama Tim: {data_tim["nama_tim"]}')
        print("Karakter:", ", ".join(data_tim["karakter"]))
        print(strip_45)

    try:
        tim_dipilih = pilih_dari_daftar(tim_saya, "Masukkan ID tim: ", "ID tim", "Tim tidak ditemukan.")
        nama_build = input("Masukkan nama konfigurasi build: ").strip()
        if not nama_build:
            raise ValueError("Nama konfigurasi tidak boleh kosong.")
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return

    karakter_build = kumpulkan_build_karakter(tim_dipilih)

    if len(karakter_build) != len(tim_dipilih["karakter"]):
        print("Konfigurasi build tidak disimpan.")
        jeda(enter_kembali_rapat)
        return

    id_build_baru = tim_dipilih["id"] + 1
    build.append({
        "id": id_build_baru,
        "username": username_aktif,
        "nama_build": nama_build,
        "id_team": tim_dipilih["id"],
        "nama_tim": tim_dipilih["nama_tim"],
        "karakter_build": karakter_build
    })
    print("\nKonfigurasi build berhasil disimpan.")
    print("ID Build:", id_build_baru)

def edit_build(username_aktif):
    bersihkan_layar()
    build_saya = ambil_build_saya(username_aktif)
    if not build_saya:
        print("Kamu belum memiliki konfigurasi build.")
        jeda(enter_kembali_rapat)
        return

    cetak_header("          EDIT KONFIGURASI BUILD", garis_45)
    for data_build in build_saya:
        print(
            f'ID: {data_build["id"]} | '
            f'Build: {data_build["nama_build"]} | '
            f'Tim: {data_build["nama_tim"]}'
        )

    try:
        build_dipilih = pilih_dari_daftar(
            build_saya, "Masukkan ID build: ", "ID build", "Build tidak ditemukan."
        )
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return

    print("\n1. Ubah nama konfigurasi")
    print("2. Ubah build satu karakter")
    pilihan_edit = minta_pilihan()

    try:
        if pilihan_edit == "1":
            nama_baru = input("Nama konfigurasi baru: ").strip()
            if not nama_baru:
                raise ValueError("Nama konfigurasi tidak boleh kosong.")
            build_dipilih["nama_build"] = nama_baru
            print("Nama konfigurasi berhasil diubah.")

        elif pilihan_edit == "2":
            cetak_ringkas_karakter(build_dipilih["karakter_build"])
            nomor_input = input("Pilih nomor karakter yang ingin diedit: ").strip()
            nomor_pilihan = baca_id(nomor_input, "Pilihan")
            if not 1 <= nomor_pilihan <= 4:
                raise ValueError("Nomor karakter tidak valid.")
            data_karakter = build_dipilih["karakter_build"][nomor_pilihan - 1]
            print("Karakter:", data_karakter["karakter"])
            senjata_baru = input("Nama senjata baru: ").strip()
            artefak_baru = input("Nama artefak baru: ").strip()
            if not (senjata_baru and artefak_baru):
                raise ValueError("Senjata dan artefak tidak boleh kosong.")
            data_karakter["senjata"] = senjata_baru
            data_karakter["artefak"] = artefak_baru
            print("Build karakter berhasil diperbarui.")

        else:
            raise ValueError("Pilihan tidak valid.")
    except (ValueError, IndexError) as e:
        print(e)
    finally:
        jeda()

def hapus_build(username_aktif):
    bersihkan_layar()
    build_saya = ambil_build_saya(username_aktif)
    if not build_saya:
        print("Kamu belum memiliki konfigurasi build.")
        jeda(enter_kembali_rapat)
        return

    cetak_header("         HAPUS KONFIGURASI BUILD", garis_45)
    for data_build in build_saya:
        print(
            f'ID: {data_build["id"]} | '
            f'{data_build["nama_build"]} | '
            f'Tim: {data_build["nama_tim"]}'
        )

    try:
        build_dipilih = pilih_dari_daftar(
            build_saya, "Masukkan ID build: ", "ID build", "Build tidak ditemukan."
        )
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return

    try:
        if any(data_tes["id_build"] == build_dipilih["id"] for data_tes in riwayat):
            raise ValueError("Build tidak dapat dihapus karena sudah digunakan dalam riwayat pengujian.")
    except ValueError as e:
        print(e)
    else:
        if konfirmasi_ya(f'Hapus konfigurasi "{build_dipilih["nama_build"]}"? (ya/tidak): '):
            build.remove(build_dipilih)
            print("Konfigurasi build berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    finally:
        jeda(enter_kembali_rapat)

def kelola_build(username_aktif):
    while True:
        bersihkan_layar()
        cetak_header("           KELOLA BUILD KARAKTER", garis_45)
        print("1. Lihat konfigurasi build")
        print("2. Buat konfigurasi build")
        print("3. Edit konfigurasi build")
        print("4. Hapus konfigurasi build")
        print("5. Kembali")
        pilihan_build = minta_pilihan()

        if pilihan_build == "1":
            lihat_build_saya(username_aktif)
        elif pilihan_build == "2":
            buat_build(username_aktif)
        elif pilihan_build == "3":
            edit_build(username_aktif)
        elif pilihan_build == "4":
            hapus_build(username_aktif)
        elif pilihan_build == "5":
            break
        else:
            print("Pilihan tidak valid.")
            jeda(enter_kembali_rapat)

# USER - CATAT HASIL PENGUJIAN DPS
def catat_tes_baru(username_aktif):
    bersihkan_layar()
    build_saya = ambil_build_saya(username_aktif)
    if not build_saya:
        print("Kamu belum memiliki konfigurasi build.")
        print("Buat konfigurasi terlebih dahulu di menu nomor 3.")
        jeda()
        return

    # Pilih build
    cetak_header("       PILIH KONFIGURASI BUILD TIM", garis_45)
    for data_build in build_saya:
        print(f'\nID Build   : {data_build["id"]}')
        print(f'Nama Build : {data_build["nama_build"]}')
        print(f'Nama Tim   : {data_build["nama_tim"]}')
        cetak_ringkas_karakter(data_build["karakter_build"])
        print(strip_45)

    try:
        build_dipilih = pilih_dari_daftar(
            build_saya, "\nMasukkan ID konfigurasi build yang diuji: ",
            "ID build", "Konfigurasi build tidak ditemukan."
        )
        # Pilih preset
        tampilkan_pilihan_preset()
        id_preset = pilih_id(preset, "\nMasukkan ID preset: ", "ID preset", "Preset tidak ditemukan.")
        # Pilih target dummy
        tampilkan_pilihan_dummy()
        id_dummy = pilih_id(dummy, "\nMasukkan ID target dummy: ", "ID dummy", "Target dummy tidak ditemukan.")
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return

    # Konfirmasi pengujian
    print("\n" + garis_45)
    print("          KONFIRMASI PENGUJIAN")
    print(garis_45)
    print("Nama Tim   :", build_dipilih["nama_tim"])
    print("Nama Build :", build_dipilih["nama_build"])
    print("Preset     :", preset[id_preset]["nama"])
    print("Target     :", dummy[id_dummy]["nama"])
    print("\nKarakter yang akan diuji:")
    cetak_ringkas_karakter(build_dipilih["karakter_build"])
    if not konfirmasi_ya("\nApakah pengujian sudah dilakukan? (ya/tidak): "):
        print("Pencatatan pengujian dibatalkan.")
        jeda(enter_kembali_rapat)
        return

    # Input hasil DPS
    try:
        hasil_dps = input("\nMasukkan hasil DPS dari game: ").strip()
        if not hasil_dps.isdigit():
            raise ValueError("Hasil DPS harus berupa angka bulat.")
        hasil_dps = int(hasil_dps)
        if hasil_dps <= 0:
            raise ValueError("Hasil DPS harus lebih besar dari 0.")
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return
    else:
        id_tes_baru = buat_id_tes()
        waktu_sekarang = waktu_tes()
        riwayat.append({
            "id": id_tes_baru,
            "username": username_aktif,
            "id_team": build_dipilih["id_team"],
            "id_build": build_dipilih["id"],
            "nama_tim": build_dipilih["nama_tim"],
            "nama_build": build_dipilih["nama_build"],
            "karakter_build": [dict(data) for data in build_dipilih["karakter_build"]],
            "id_preset": id_preset,
            "id_dummy": id_dummy,
            "dps": hasil_dps,
            "waktu": waktu_sekarang
        })
        print("\nPengujian DPS berhasil dicatat.")
        print("ID Tes     :", id_tes_baru)
        print("Waktu      :", waktu_sekarang)
        print("Nama Tim   :", build_dipilih["nama_tim"])
        print("Nama Build :", build_dipilih["nama_build"])
        print("Hasil DPS  :", format_ribuan(hasil_dps))
    jeda()

def menu_catat_dps(username_aktif):
    while True:
        bersihkan_layar()
        cetak_header("          CATAT HASIL PENGUJIAN DPS", garis_45)
        print("1. Catat tes baru")
        print("2. Kembali")
        pilihan_tes = minta_pilihan()

        if pilihan_tes == "2":
            break
        if pilihan_tes != "1":
            print("Pilihan tidak valid.")
            jeda()
            continue
        catat_tes_baru(username_aktif)

# USER - RIWAYAT PENGUJIAN
def lihat_daftar_riwayat(username_aktif):
    bersihkan_layar()
    cetak_header("                 DAFTAR RIWAYAT DPS", garis_55)
    riwayat_saya = ambil_riwayat_saya(username_aktif)

    if not riwayat_saya:
        print("Kamu belum memiliki riwayat pengujian DPS.")
    else:
        for data_tes in riwayat_saya:
            preset_dipilih = preset.get(data_tes["id_preset"])
            dummy_dipilih = dummy.get(data_tes["id_dummy"])
            waktu_tes = data_tes.get("waktu", "Tidak diketahui")

            print(f'\nID Tes       : {data_tes["id"]}')
            print(f'Waktu Tes    : {waktu_tes}')
            print(f'Nama Tim     : {data_tes["nama_tim"]}')
            print(f'Nama Build   : {data_tes["nama_build"]}')
            print("Preset       :", preset_dipilih["nama"] if preset_dipilih else "Preset tidak ditemukan")
            print("Target Dummy :", dummy_dipilih["nama"] if dummy_dipilih else "Dummy tidak ditemukan")
            print("Hasil DPS    :", format_ribuan(data_tes["dps"]))
            print(strip_55)
    jeda()

def lihat_detail_riwayat(username_aktif):
    bersihkan_layar()
    cetak_header("                 DETAIL RIWAYAT DPS", garis_55)
    riwayat_saya = ambil_riwayat_saya(username_aktif)
    if not riwayat_saya:
        print("Kamu belum memiliki riwayat pengujian DPS.")
        jeda()
        return

    for data_tes in riwayat_saya:
        print(
            f'ID Tes: {data_tes["id"]} | '
            f'{data_tes["nama_tim"]} | '
            f'{data_tes["nama_build"]} | '
            f'DPS: {format_ribuan(data_tes["dps"])}'
        )

    try:
        tes_dipilih = pilih_dari_daftar(
            riwayat_saya, "\nMasukkan ID tes yang ingin dilihat: ",
            "ID tes", "Riwayat pengujian tidak ditemukan."
        )
    except ValueError as e:
        print(e)
        jeda(enter_kembali_rapat)
        return

    bersihkan_layar()
    preset_dipilih = preset.get(tes_dipilih["id_preset"])
    dummy_dipilih = dummy.get(tes_dipilih["id_dummy"])

    cetak_header("                 DETAIL PENGUJIAN DPS", garis_55)
    print("ID Tes       :", tes_dipilih["id"])
    print("Nama Tim     :", tes_dipilih["nama_tim"])
    print("Nama Build   :", tes_dipilih["nama_build"])
    print("Preset       :", preset_dipilih["nama"] if preset_dipilih else "Preset tidak ditemukan")
    if preset_dipilih:
        print("Deskripsi    :", preset_dipilih["deskripsi"])
    print("Target Dummy :", dummy_dipilih["nama"] if dummy_dipilih else "Dummy tidak ditemukan")
    if dummy_dipilih:
        print("Kategori     :", dummy_dipilih["kategori"])
        print("Deskripsi    :", dummy_dipilih["deskripsi"])
    print("\nKONFIGURASI BUILD SAAT PENGUJIAN")
    print(strip_55)
    for nomor, data_karakter in enumerate(tes_dipilih["karakter_build"], start=1):
        cetak_karakter_build(nomor, data_karakter, lebar_label=8)
    print("\n" + garis_55)
    print("HASIL DPS:", format_ribuan(tes_dipilih["dps"]))
    print(garis_55)
    jeda()

def menu_riwayat(username_aktif):
    while True:
        bersihkan_layar()
        cetak_header("                 RIWAYAT PENGUJIAN DPS", garis_55)
        print("1. Lihat seluruh riwayat")
        print("2. Lihat detail riwayat")
        print("3. Kembali")
        pilihan_riwayat = minta_pilihan()

        if pilihan_riwayat == "1":
            lihat_daftar_riwayat(username_aktif)
        elif pilihan_riwayat == "2":
            lihat_detail_riwayat(username_aktif)
        elif pilihan_riwayat == "3":
            break
        else:
            print("Pilihan tidak valid.")
            jeda("Tekan Enter untuk melanjutkan...")

def lihat_preset():
    bersihkan_layar()
    cetak_header("             PRESET PENGUJIAN DPS", garis_55)

    if not preset:
        print("Belum ada preset pengujian.")
    else:
        tabel_p = buat_tabel_preset()
        for id_item, data_preset in preset.items():
            tabel_p.add_row([id_item, data_preset["nama"], data_preset["deskripsi"]])
        print(tabel_p)
    jeda()

def lihat_dummy():
    bersihkan_layar()
    cetak_header("                TARGET DUMMY", garis_55)

    if not dummy:
        print("Belum ada target dummy.")
    else:
        tabel_d = buat_tabel_dummy()
        for id_item, data_dummy in dummy.items():
            tabel_d.add_row([id_item, data_dummy["nama"], data_dummy["kategori"], data_dummy["deskripsi"]])
        print(tabel_d)
    jeda()

# MENU USER
def menu_user(username_aktif):
    while True:
        bersihkan_layar()
        cetak_header("           MENU USER", garis_40)
        print("Login sebagai:", username_aktif)
        print("1. Lihat daftar karakter")
        print("2. Kelola tim")
        print("3. Kelola build karakter")
        print("4. Catat hasil pengujian DPS")
        print("5. Lihat riwayat pengujian")
        print("6. Lihat preset")
        print("7. Lihat dummy")
        print("8. Logout")
        pilihan_user = minta_pilihan()

        if pilihan_user == "1":
            lihat_daftar_karakter()
        elif pilihan_user == "2":
            kelola_tim(username_aktif)
        elif pilihan_user == "3":
            kelola_build(username_aktif)
        elif pilihan_user == "4":
            menu_catat_dps(username_aktif)
        elif pilihan_user == "5":
            menu_riwayat(username_aktif)
        elif pilihan_user == "6":
            lihat_preset()
        elif pilihan_user == "7":
            lihat_dummy()
        elif pilihan_user == "8":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
            jeda()
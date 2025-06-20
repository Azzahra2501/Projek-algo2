import pandas as pd
import csv
import os
from datetime import datetime
from tabulate import tabulate
from collections import defaultdict
import heapq

CSV_FILE = "Generate by Sistem.csv"
USER_FILE = "User.csv"

# ==================== LOGIN ====================
def login():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 60)
        print("Selamat Datang di Sistem Manajemen Obat Apotek".center(60))
        print("=" * 60)
        print("\nSilakan masukkan Username dan Password Anda!\n")
        username = input("Username: ")
        password = input("Password: ")

        try:
            df_users = pd.read_csv(USER_FILE)
            df_users.columns = [col.strip() for col in df_users.columns]
            user_valid = df_users[(df_users['Username'] == username) & (df_users['Password'] == password)]

            if not user_valid.empty:
                print(f"\nLogin berhasil. Selamat datang, {username}!\n")
                while True:
                    lanjut = input("Tekan Enter untuk melanjutkan...")
                    if lanjut == "":
                        break
                    else:
                        print("Harap tekan Enter tanpa mengetik apa pun.")
                return True
            else:
                print("\nUsername atau password salah.")
                pilihan = input("1. Coba Lagi\n2. Keluar\nPilih: ")
                if pilihan == "2":
                    print("Keluar dari sistem...")
                    return False
        except FileNotFoundError:
            print(f"\nFile '{USER_FILE}' tidak ditemukan. Hubungi admin.")
            return False

# ==================== MENU UTAMA ====================
def menu_utama():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("============================")
        print("         Menu Utama         ")
        print("============================")
        print("1. Kelola Obat")
        print("2. Cek Stok Obat")
        print("3. Cek Kadaluarsa")
        print("4. Keluar")

        pilihan = input("Pilih menu (1/2/3): ").strip()
        if pilihan == '1':
            kelola_obat()
        elif pilihan == '2':
            menu_cek_stok()
        elif pilihan == '3':
            main_kadaluarsa()
        elif pilihan == '4':
            print("Terima kasih telah menggunakan sistem.")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")

# ==================== SUBMENU CEK STOK OBAT ====================
def menu_cek_stok():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("===============================")
        print("          Cek Stok Obat        ")
        print("===============================")
        print("1. Search by Name")
        print("2. Generate by Sistem (Update Total Stok & Rekomendasi Restock)")
        print("3. Kembali ke Menu Utama")

        pilihan = input("Pilih menu (1/2/3): ").strip()
        if pilihan == '1':
            cek_stok_by_nama()
        elif pilihan == '2':
            generate_rekomendasi_stok()
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")

# ==================== SUBMENU KELOLA OBAT ====================
def kelola_obat():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("===============================")
        print("          Kelola Obat          ")
        print("===============================")
        print("1. Menambah Data Obat")
        print("2. Lihat Data Obat")
        print("3. Kurangi Stok Obat")
        print("4. Hapus Data Obat")
        print("5. Kembali ke Menu Utama")

        pilihan = input("Pilih menu (1/2/3/4): ").strip()
        if pilihan == '1':
            tambah_data_obat()
        elif pilihan == '2':
            lihat_data_obat()
        elif pilihan == '3':
            kurangi_stok()
        elif pilihan == '4':
           fitur_hapus_obat()
        elif pilihan == '5':
            input("Tekan Enter untuk kembali ke menu...")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk lanjut...")

# ==================== LIHAT DATA OBAT ====================
def baca_data():
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"File '{CSV_FILE}' tidak ditemukan.")
        return []

def simpan_data(data):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Kode Obat', 'Nama', 'Jenis', 'Tanggal Datang',
                      'Jumlah Stok', 'Total Stok', 'Rekomendasi Restock', 'Tanggal Kadaluarsa']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def tampilkan_data(data):
    if not data:
        print("Tidak ada data untuk ditampilkan.")
        return
    tabel = [[
        d['Kode Obat'], d['Nama'], d['Jenis'], d['Tanggal Datang'],
        d['Jumlah Stok'], d['Total Stok'], d['Rekomendasi Restock'], d.get('Tanggal Kadaluarsa', '')
    ] for d in data]
    print(tabulate(tabel, headers=[
        "Kode Obat", "Nama", "Jenis", "Tanggal Datang",
        "Jumlah Stok", "Total Stok", "Rekomendasi Restock", "Tanggal Kadaluarsa"
    ], tablefmt="grid"))

def lihat_data_obat():
    os.system("cls" if os.name == "nt" else "clear")
    data = baca_data()
    if not data:
        input("Tekan Enter untuk kembali ke menu...")
        return
    df = pd.DataFrame(data)
    df.columns = [col.strip() for col in df.columns]

    try:
        df_unique = df.drop_duplicates(subset=['Kode Obat'])
        print("\nDaftar Obat (Kode Obat, Nama, Jenis):\n")
        print(tabulate(df_unique[['Kode Obat', 'Nama', 'Jenis']], headers='keys', tablefmt='pretty', showindex=False))
    except KeyError as e:
        print(f"Kesalahan kolom: {e}. Pastikan nama kolom sesuai.")
    input("\nTekan Enter untuk kembali ke menu...")

# ==================== MENAMBAH DATA OBAT ================================
def baca_data():
    data = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Kode Obat', 'Nama', 'Jenis', 'Tanggal Datang', 'Jumlah Stok', 'Total Stok', 'Rekomendasi Restock', 'Tanggal Kadaluarsa'])
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['Jumlah Stok'] = int(row['Jumlah Stok'])
            except (ValueError, KeyError):
                row['Jumlah Stok'] = 0
            try:
                row['Total Stok'] = int(row.get('Total Stok', 0))
            except (ValueError, KeyError):
                row['Total Stok'] = 0
            row.setdefault('Rekomendasi Restock', '')  
            data.append(row)
    return data

def simpan_data(data):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['Kode Obat', 'Nama', 'Jenis', 'Tanggal Datang', 'Jumlah Stok', 'Total Stok', 'Rekomendasi Restock', 'Tanggal Kadaluarsa']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def tampilkan_data(data):
    if not data:
        print("Tidak ada data obat.")
        return
    tabel = [[
        d['Kode Obat'], d['Nama'], d['Jenis'], d['Tanggal Datang'], d['Jumlah Stok'],
        d['Total Stok'], d['Rekomendasi Restock'], d['Tanggal Kadaluarsa']
    ] for d in data]
    headers = ['Kode', 'Nama', 'Jenis', 'Tgl Datang', 'Stok Masuk', 'Total Stok', 'Restock?', 'Tgl Exp']
    print(tabulate(tabel, headers=headers, tablefmt='grid'))

def update_total_stok(data):
    total_per_nama = {}
    for item in data:
        nama = item.get('Nama', '').strip().capitalize()
        try:
            jumlah_stok = int(item.get('Jumlah Stok', 0))
        except ValueError:
            jumlah_stok = 0
        total_per_nama[nama] = total_per_nama.get(nama, 0) + jumlah_stok

    for item in data:
        nama = item.get('Nama', '').strip().capitalize()
        total = total_per_nama.get(nama, 0)
        item['Total Stok'] = total
        item['Rekomendasi Restock'] = 'Ya' if total < 20 else 'Tidak'

def tambah_data_obat():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Tambah Data Obat ===")
        data = baca_data()

        kode = input("Kode Obat (OBxxx): ").strip().upper()
        if kode == "":
            print("Batal menambahkan data.\n")
            keluar = input("Ketik 'y' untuk keluar atau Enter untuk mulai lagi: ").strip().lower()
            if keluar == 'y':
                break
            else:
                continue

        if not (len(kode) == 5 and kode.startswith('OB') and kode[2:].isdigit()):
            print("Format kode salah. Contoh: OB001")
            input("Tekan Enter untuk coba lagi...")
            continue

        nama = input("Nama Obat: ").strip().capitalize()
        if nama == "":
            print("Batal menambahkan data.\n")
            keluar = input("Ketik 'y' untuk keluar atau Enter untuk mulai lagi: ").strip().lower()
            if keluar == 'y':
                break
            else:
                continue

        jenis = input("Jenis Obat: ").strip().capitalize()
        if jenis == "":
            print("Batal menambahkan data.\n")
            keluar = input("Ketik 'y' untuk keluar atau Enter untuk mulai lagi: ").strip().lower()
            if keluar == 'y':
                break
            else:
                continue

        try:
            tanggal_datang = datetime.strptime(input("Tanggal Datang (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("Format tanggal salah!")
            input("Tekan Enter untuk coba lagi...")
            continue

        try:
            jumlah = int(input("Jumlah Stok Masuk: ").strip())
            if jumlah <= 0:
                print("Jumlah harus lebih dari nol.")
                input("Tekan Enter untuk coba lagi...")
                continue
        except ValueError:
            print("Input jumlah tidak valid.")
            input("Tekan Enter untuk coba lagi...")
            continue

        try:
            tanggal_kadaluarsa = datetime.strptime(input("Tanggal Kadaluarsa (YYYY-MM-DD): ").strip(), "%Y-%m-%d").date()
        except ValueError:
            print("Format tanggal kadaluarsa salah!")
            input("Tekan Enter untuk coba lagi...")
            continue

        # Tampilkan data untuk konfirmasi
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Konfirmasi Data Obat ===")
        print(f"Kode Obat        : {kode}")
        print(f"Nama Obat        : {nama}")
        print(f"Jenis Obat       : {jenis}")
        print(f"Tanggal Datang   : {tanggal_datang}")
        print(f"Jumlah Stok Masuk: {jumlah}")
        print(f"Tanggal Kadaluarsa: {tanggal_kadaluarsa}")
        print("\n")

        konfirmasi = input("Ketik 'simpan' untuk menyimpan, atau Enter untuk batal: ").strip().lower()
        if konfirmasi == 'simpan':
            data.append({
                'Kode Obat': kode,
                'Nama': nama,
                'Jenis': jenis,
                'Tanggal Datang': str(tanggal_datang),
                'Jumlah Stok': jumlah,
                'Total Stok': 0,
                'Rekomendasi Restock': '',
                'Tanggal Kadaluarsa': str(tanggal_kadaluarsa)
            })
            update_total_stok(data)
            simpan_data(data)
            print("\nData berhasil disimpan.")
        else:
            print("Data tidak disimpan.")

        lanjut = input("\nKetik 'y' untuk menambahkan obat lagi atau tekan Enter untuk kembali ke menu: ").strip().lower()
        if lanjut != 'y':
            break


def baca():
    data = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Rekomendasi Restock' in row:
                    del row['Rekomendasi Restock']
                data.append(row)
    except FileNotFoundError:
        print(f"File '{CSV_FILE}' tidak ditemukan.")
    return data


# ======================== KURANGI STOK ============================
def baca():
    data = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Rekomendasi Restock' in row:
                    del row['Rekomendasi Restock']
                data.append(row)
    except FileNotFoundError:
        print(f"File '{CSV_FILE}' tidak ditemukan.")
    return data


def simpan_data(data):
    if not data:
        return
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def tampilkan_data(data):
    if not data:
        print("Data kosong.")
        return
    print(tabulate(data, headers="keys", tablefmt="grid"))


def cari_data(data, kode, tanggal):
    return [item for item in data if item['Kode Obat'] == kode and item['Tanggal Datang'] == tanggal]

def update_stok(data, kode, tanggal, pengurangan):
    for item in data:
        if item['Kode Obat'] == kode and item['Tanggal Datang'] == tanggal:
            jumlah_sekarang = int(item['Jumlah Stok'])
            if pengurangan > jumlah_sekarang:
                print("Pengurangan melebihi jumlah stok yang tersedia.")
                return False
            item['Jumlah Stok'] = str(jumlah_sekarang - pengurangan)
            break
    else:
        return False

    total_baru = sum(int(i['Jumlah Stok']) for i in data if i['Kode Obat'] == kode)
    for item in data:
        if item['Kode Obat'] == kode:
            item['Total Stok'] = str(total_baru)

    return True

def kurangi_stok():
    while True:
        data = baca()
        print("\n=== Data Obat Saat Ini ===")
        tampilkan_data(data)

        print("\n--- Kurangi Stok Obat ---")
        kode = input("Masukkan Kode Obat: ").strip()
        tanggal = input("Masukkan Tanggal Datang (YYYY-MM-DD): ").strip()

        hasil = cari_data(data, kode, tanggal)

        if hasil:
            print("\nData ditemukan:")
            tampilkan_data(hasil)

            try:
                pengurangan = int(input("Masukkan jumlah pengurangan stok: "))
                if pengurangan < 0:
                    print("Jumlah tidak boleh negatif.")
                    continue
            except ValueError:
                print("Input harus berupa angka.")
                continue

            berhasil = update_stok(data, kode, tanggal, pengurangan)
            if berhasil:
                simpan_data(data)
                print("Stok berhasil dikurangi.")
                print("\n=== Data Obat Setelah Perubahan ===")
                data = baca_data()
                tampilkan_data(data)
            else:
                print("Gagal memperbarui stok. Cek apakah stok cukup atau data valid.")

            keluar = input("Ketik 'y' untuk keluar dari menu atau tekan enter untuk lanjut: ").strip().lower()
            if keluar == 'y':
                break
        else:
            print("Data tidak ditemukan.")
            pilihan = input("Ketik '1' untuk coba lagi atau '2' untuk keluar: ").strip()
            if pilihan == '2':
                break


# ==================== FUNGSI HAPUS DATA ====================
def load_obat_dari_csv(nama_file):
    data_obat = []
    try:
        with open(nama_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Rekomendasi Restock' in row:
                    del row['Rekomendasi Restock']

                data_obat.append(row)
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan.")
    return data_obat

def simpan_obat_ke_csv(nama_file, data_obat):
    with open(nama_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Kode Obat', 'Nama', 'Jenis', 'Tanggal Datang', 'Jumlah Stok', 'Total Stok', 'Tanggal Kadaluarsa']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data_obat:
            writer.writerow(row)

def tampilkan_tabel(data_obat):
    if not data_obat:
        print("Data obat kosong.")
        return
    print(tabulate(data_obat, headers="keys", tablefmt='grid'))

def cari_dan_hapus_obat(data_obat, kode_obat, tanggal_datang):
    index_dihapus = -1
    for i, obat in enumerate(data_obat):
        if obat['Kode Obat'] == kode_obat and obat['Tanggal Datang'] == tanggal_datang:
            index_dihapus = i
            break
    if index_dihapus != -1:
        print("\nObat ditemukan dan akan dihapus:")
        print(tabulate([data_obat[index_dihapus]], headers="keys", tablefmt='grid'))
        del data_obat[index_dihapus]
        print("Obat berhasil dihapus.\n")
        return True
    else:
        print("\nObat tidak ditemukan dengan Kode dan Tanggal tersebut.")
        return False

def fitur_hapus_obat():
    nama_file = 'Generate by Sistem.csv'

    while True:
        print("\n===DATA OBAT SAAT INI ===")
        data_obat = load_obat_dari_csv(nama_file)
        tampilkan_tabel(data_obat)

        if not data_obat:
            print("Tidak ada data untuk dihapus.")
            break

        print("\n=== 🗑 HAPUS DATA OBAT ===")
        kode_obat = input("Masukkan Kode Obat yang ingin dihapus: ").strip()
        tanggal_datang = input("Masukkan Tanggal Datang (YYYY-MM-DD): ").strip()

        ditemukan = cari_dan_hapus_obat(data_obat, kode_obat, tanggal_datang)

        if ditemukan:
            simpan_obat_ke_csv(nama_file, data_obat)
            lagi = input("Ingin menghapus obat lain? (y/n): ").strip().lower()
            if lagi != 'y':
                print("Keluar dari fitur hapus obat.")
                break
        else:
            coba = input("Data tidak ditemukan. Coba lagi? (y/n): ").strip().lower()
            if coba != 'y':
                print("Keluar dari fitur hapus obat.")
                break

# ==================== CEK STOK BY NAMA ====================
def cek_stok_by_nama():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Cek Stok Obat Berdasarkan Nama ===")

        nama_dicari = input("Masukkan nama obat yang ingin dicari: ").strip().lower()

        if not nama_dicari:
            print("Nama obat tidak boleh kosong.")
            ulang = input("Ingin coba lagi? (y/n): ").strip().lower()
            if ulang != 'y':
                break
            else:
                continue

        data = baca_data()
        if not data:
            print("Data obat kosong atau file tidak ditemukan.")
            input("Tekan Enter untuk kembali ke menu...")
            return

        hasil = []
        for item in data:
            try:
                nama_obat = item.get('Nama', '').lower()
                if nama_dicari in nama_obat:
                    hasil.append(item)
            except AttributeError:
                continue  

        if hasil:
            tampilkan_data(hasil)
            try:
                total = sum(int(item.get('Jumlah Stok', 0)) for item in hasil)
                print(f"\nTotal stok: {total}")
            except ValueError:
                print("\nAda data jumlah stok yang tidak valid.")
            input("\nTekan Enter untuk kembali ke menu...")
            break  
        else:
            print(f"Obat dengan nama '{nama_dicari}' tidak ditemukan.")
            ulang = input("Ingin coba cari lagi? (y/n): ").strip().lower()
            if ulang != 'y':
                break


# ==================== GENERATE BY SISTEM ====================
def heapify(arr, n, i):
    smallest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and int(arr[l]['Total Stok']) < int(arr[smallest]['Total Stok']):
        smallest = l
    if r < n and int(arr[r]['Total Stok']) < int(arr[smallest]['Total Stok']):
        smallest = r

    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify(arr, n, smallest)

def heap_sort_by_total_stok(arr):
    n = len(arr)

    # Bangun min heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Ekstrak elemen dari heap satu per satu
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Tukar elemen pertama dan terakhir
        heapify(arr, i, 0)

    # Balik hasil karena kita pakai min-heap dan mau urutan dari kecil ke besar
    arr.reverse()
    return arr

def cek_stok_dan_generate_rekomendasi_heapsort(data):
    total_stok_per_obat = defaultdict(int)

    # Hitung total stok untuk tiap nama obat
    for d in data:
        total_stok_per_obat[d['Nama']] += int(d['Jumlah Stok'])

    # Tambahkan kolom total stok ke setiap entri
    for d in data:
        nama_obat = d['Nama']
        total_stok = total_stok_per_obat[nama_obat]
        d['Total Stok'] = str(total_stok)

    # Tambahkan rekomendasi restock
    for d in data:
        d['Rekomendasi Restock'] = 'Ya' if int(d['Total Stok']) < 20 else 'Tidak'

    # Urutkan seluruh data dengan heap sort berdasarkan total stok
    data_terurut = heap_sort_by_total_stok(data)

    return data_terurut

def generate_rekomendasi_stok():
    data = baca_data()
    if not data:
        input("File data kosong atau tidak ditemukan. Tekan Enter untuk kembali!")
        return

    data_diperbarui = cek_stok_dan_generate_rekomendasi_heapsort(data)
    simpan_data(data_diperbarui)

    print("\n=== Generate by Sistem: Cek Stok (Heap Sort Manual) ===")
    tampilkan_data(data_diperbarui)

#============================ CEK KADALUARSA ========================================
def main_kadaluarsa():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== Cek Obat Kadaluarsa ===")

    data_mentah = baca_data()
    if not data_mentah:
        print("Data obat kosong.")
        input("Tekan Enter untuk kembali ke menu...")
        return

    grouped = defaultdict(list)

    for item in data_mentah:
        nama = item['Nama'].strip()
        try:
            tgl = datetime.strptime(item['Tanggal Kadaluarsa'].strip(), "%Y-%m-%d").date()
            grouped[nama].append(tgl)
        except:
            continue

    for nama, daftar_tanggal in grouped.items():
        daftar_tanggal.sort()
        print(f"\nMemeriksa Obat: {nama}")
        dfs_tanggal_kadaluarsa(nama, daftar_tanggal, 0)

    input("\nTekan Enter untuk kembali ke menu...")

def dfs_tanggal_kadaluarsa(nama_obat, daftar_tanggal, index):
    if index >= len(daftar_tanggal) or index >= 2:
        return

    tanggal = daftar_tanggal[index]
    status = "KADALUARSA" if tanggal < datetime.today().date() else "AMAN"
    print(f"  - Batch {index+1}: {tanggal.strftime('%d-%m-%Y')} ({status})")

    dfs_tanggal_kadaluarsa(nama_obat, daftar_tanggal, index + 1)

def baca_data():
    nama_file = "Generate by Sistem.csv"
    data = []
    try:
        with open(nama_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File '{nama_file}' tidak ditemukan.")
    return data

# =================== MAIN ====================
if __name__ == "__main__":
    if login():
        menu_utama()
    else:
        print("Program dihentikan.")


"""ch16_uji_mandiri.py — Pemeriksa level secara otomatis.

Menjalankan tiga pemeriksaan atas sebuah level platformer, tanpa pemain:

  1. Keterjangkauan  — dapatkah titik tujuan dicapai dari setiap tempat
                        pemain dapat berdiri? Tempat yang tidak dapat
                        mencapai tujuan adalah calon soft-lock.
  2. Lompatan mustahil — jarak setiap celah dibandingkan dengan jangkauan
                        lompatan yang dihitung dari besaran fisika.
  3. Simulasi tanpa pemain — titik awal diacak berulang kali, lalu dihitung
                        berapa persen yang berhasil mencapai tujuan.

Model geraknya disederhanakan: pemain dianggap selalu berlari dengan
kecepatan penuh dan melompat pada saat yang paling menguntungkan. Jadi
jangkauan yang dihitung adalah jangkauan TERBESAR. Sebuah petak yang tidak
terjangkau oleh model ini pasti juga tidak terjangkau oleh pemain, sehingga
pemeriksa ini aman dipakai untuk mencari soft-lock. Sebaliknya, petak yang
terjangkau oleh model ini belum tentu mudah dicapai pemain.

Jalankan:  python -I ch16_uji_mandiri.py --help
           python -I ch16_uji_mandiri.py --peta terjebak
"""

import argparse
import heapq
import math
import random
import statistics
import sys

# ---------------------------------------------------------------- Fisika
# Besaran yang sama dengan Bab VI dan Bab XIII. Satuannya piksel dan detik.
GRAVITASI = 1800.0
KECEPATAN_LOMPAT = 700.0
KECEPATAN_JALAN = 300.0
UKURAN_PETAK = 32.0


def tinggi_maksimum() -> float:
    """Tinggi lompatan tertinggi, dalam piksel: v0^2 / (2g)."""
    return KECEPATAN_LOMPAT ** 2 / (2 * GRAVITASI)


def lama_di_udara(beda_tinggi: float) -> float:
    """Lama pemain berada di udara menuju beda_tinggi, dalam detik.

    beda_tinggi bernilai positif apabila tujuannya lebih tinggi. Nilai yang
    dipakai adalah akar yang lebih besar, yaitu saat pemain sedang turun,
    sebab di situlah jarak mendatarnya paling jauh.
    """
    dalam_akar = KECEPATAN_LOMPAT ** 2 - 2 * GRAVITASI * beda_tinggi
    if dalam_akar < 0:
        return -1.0            # ketinggian itu tidak mungkin dicapai
    return (KECEPATAN_LOMPAT + math.sqrt(dalam_akar)) / GRAVITASI


def jangkauan_mendatar(beda_tinggi: float) -> float:
    """Jarak mendatar terjauh menuju beda_tinggi, dalam piksel."""
    lama = lama_di_udara(beda_tinggi)
    if lama < 0:
        return -1.0
    return KECEPATAN_JALAN * lama


def bisa_menyeberang(beda_kolom: int, beda_baris: int) -> bool:
    """Dapatkah pemain melompat dari satu pijakan ke pijakan lain?

    beda_baris bernilai positif apabila tujuannya lebih tinggi pada peta,
    sebab baris pada peta bertambah ke bawah.
    """
    beda_tinggi = -beda_baris * UKURAN_PETAK      # ke atas bernilai positif
    if beda_tinggi > tinggi_maksimum():
        return False
    jangkauan = jangkauan_mendatar(beda_tinggi)
    if jangkauan < 0:
        return False
    jarak = abs(beda_kolom) * UKURAN_PETAK
    return jarak <= jangkauan


# ---------------------------------------------------------------- Peta
# '#' dinding, '.' ruang kosong, 'S' titik awal, 'G' titik tujuan.
PETA = {
    # Seluruh tempat berdiri dapat mencapai tujuan. Level ini acuan yang
    # seharusnya Anda tiru.
    "rapi": (
        "##############################",
        "#............................#",
        "#..S.........................#",
        "#####........................#",
        "#............................#",
        "#............................#",
        "#....######..................#",
        "#............................#",
        "#............................#",
        "#..........######............#",
        "#........................G...#",
        "##############################",
    ),
    # Tujuannya diletakkan di atas tiang yang terlalu tinggi dan terlalu
    # jauh untuk dicapai, sehingga tidak seorang pun dapat menyelesaikannya.
    "sempit": (
        "##############################",
        "#............................#",
        "#..S................G........#",
        "#####...............#........#",
        "#............................#",
        "#............................#",
        "#....######..................#",
        "#............................#",
        "#............................#",
        "#..........######............#",
        "#............................#",
        "##############################",
    ),
    # Tujuan dapat dicapai, tetapi ada lubang yang tidak dapat ditinggalkan
    # pemain. Pemain yang terlanjur jatuh ke sana tidak dapat melanjutkan
    # permainan, walaupun programnya tidak berhenti.
    "terjebak": (
        "##############################",
        "#............................#",
        "#..S.........................#",
        "#####........................#",
        "#............................#",
        "#............................#",
        "#.....#......................#",
        "#.....#......................#",
        "#.....#......................#",
        "#.....#......................#",
        "#.....#.....................G#",
        "##############################",
    ),
}


def baca_peta(peta: tuple) -> tuple:
    """Membaca peta menjadi himpunan dinding, titik awal, dan titik tujuan."""
    lebar = len(peta[0])
    for nomor, baris in enumerate(peta, start=1):
        if len(baris) != lebar:
            raise ValueError(
                f"baris {nomor} panjangnya {len(baris)} petak, "
                f"sedangkan baris pertama {lebar} petak")

    dinding = set()
    awal = tujuan = None
    for baris, isi in enumerate(peta):
        for kolom, huruf in enumerate(isi):
            if huruf == "#":
                dinding.add((kolom, baris))
            elif huruf == "S":
                awal = (kolom, baris)
            elif huruf == "G":
                tujuan = (kolom, baris)

    if awal is None or tujuan is None:
        raise ValueError("peta harus memuat satu 'S' dan satu 'G'")
    return dinding, awal, tujuan


def pijakan(peta: tuple, dinding: set) -> list:
    """Daftar petak tempat pemain dapat berdiri, yaitu petak kosong yang
    bawahnya berupa dinding."""
    tinggi, lebar = len(peta), len(peta[0])
    hasil = []
    for baris in range(tinggi - 1):
        for kolom in range(lebar):
            if (kolom, baris) in dinding:
                continue
            if (kolom, baris + 1) in dinding:
                hasil.append((kolom, baris))
    return hasil


def lantai_di_bawah(peta: tuple, dinding: set, petak: tuple) -> tuple:
    """Petak pijakan terdekat di bawah petak ini, atau None apabila kosong."""
    kolom, baris = petak
    for bawah in range(baris + 1, len(peta)):
        if (kolom, bawah) in dinding:
            return (kolom, bawah - 1) if bawah - 1 > baris else None
    return None


def tetangga(peta: tuple, dinding: set, daftar_pijakan: list,
             petak: tuple) -> list:
    """Seluruh pijakan yang dapat dicapai dari satu pijakan.

    Empat jalan yang tersedia: berjalan ke kiri atau ke kanan pada pijakan
    yang sama, jatuh ke pijakan di bawahnya, dan melompat ke pijakan lain
    yang masih terjangkau.
    """
    kolom, baris = petak
    hasil = []

    # Berjalan ke kiri dan ke kanan, selama tidak ada dinding.
    for arah in (-1, 1):
        sekarang = (kolom + arah, baris)
        while ((sekarang not in dinding)
               and ((sekarang[0], sekarang[1] + 1) in dinding)):
            hasil.append(sekarang)
            sekarang = (sekarang[0] + arah, sekarang[1])

    # Melompat dan jatuh ke setiap pijakan yang lain.
    for lain in daftar_pijakan:
        if lain == petak:
            continue
        beda_kolom = lain[0] - kolom
        beda_baris = lain[1] - baris
        if bila_terhalang(dinding, petak, lain):
            continue
        if bisa_menyeberang(beda_kolom, beda_baris):
            hasil.append(lain)

    return hasil


def bila_terhalang(dinding: set, dari: tuple, ke: tuple) -> bool:
    """Perkiraan kasar: lompatan dianggap terhalang apabila lintasan
    lurus antara kedua pijakan melewati dinding."""
    langkah = max(abs(ke[0] - dari[0]), abs(ke[1] - dari[1]))
    if langkah == 0:
        return False
    for i in range(1, langkah):
        kolom = round(dari[0] + (ke[0] - dari[0]) * i / langkah)
        baris = round(dari[1] + (ke[1] - dari[1]) * i / langkah)
        if (kolom, baris) in dinding:
            return True
    return False


def cari_jalur(peta: tuple, dinding: set, daftar_pijakan: list,
               awal: tuple, tujuan: tuple, batas: int = 0) -> dict:
    """Mencari jalur terpendek pada graf pijakan dengan algoritma A*.

    Algoritmanya sama dengan Bab X. Yang berbeda hanya aturan tetangganya:
    di sini tetangga sebuah pijakan adalah pijakan lain yang dapat dicapai
    dengan berjalan, jatuh, atau melompat.
    """
    def perkiraan(a: tuple, b: tuple) -> float:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    antrean = [(perkiraan(awal, tujuan), 0.0, awal)]
    asal = {awal: None}
    biaya = {awal: 0.0}
    diperiksa = 0

    while antrean:
        _, biaya_kini, sekarang = heapq.heappop(antrean)
        if sekarang == tujuan:
            jalur = []
            while sekarang is not None:
                jalur.append(sekarang)
                sekarang = asal[sekarang]
            jalur.reverse()
            return {"jalur": jalur, "diperiksa": diperiksa, "biaya": biaya_kini}

        if biaya_kini > biaya.get(sekarang, float("inf")):
            continue
        diperiksa += 1

        if batas and diperiksa > batas:
            return {"jalur": None, "diperiksa": diperiksa, "biaya": 0.0}

        for lain in tetangga(peta, dinding, daftar_pijakan, sekarang):
            biaya_baru = biaya_kini + 1.0
            if biaya_baru < biaya.get(lain, float("inf")):
                biaya[lain] = biaya_baru
                asal[lain] = sekarang
                heapq.heappush(antrean,
                               (biaya_baru + perkiraan(lain, tujuan),
                                biaya_baru, lain))

    return {"jalur": None, "diperiksa": diperiksa, "biaya": 0.0}


# ---------------------------------------------------------------- Laporan
def periksa_keterjangkauan(peta: tuple, dinding: set, daftar_pijakan: list,
                           tujuan: tuple) -> tuple:
    """Memeriksa setiap pijakan; mengembalikan yang tidak dapat mencapai
    tujuan beserta jangkauan terbaik yang dimilikinya."""
    terjebak = []
    for petak in daftar_pijakan:
        hasil = cari_jalur(peta, dinding, daftar_pijakan, petak, tujuan)
        if hasil["jalur"] is None:
            terjebak.append(petak)
    return terjebak


def jalan_ke_atas(peta: tuple, dinding: set, daftar_pijakan: list,
                  petak: tuple) -> tuple:
    """Pijakan terdekat yang lebih tinggi dan dapat dicapai, atau None.

    Pemeriksaan ini berbeda dari pemeriksaan keterjangkauan. Yang dicari di
    sini bukan apakah tujuan dapat dicapai, melainkan apakah pemain yang
    berada di petak ini masih dapat berpindah ke tempat yang lebih tinggi.
    Tempat yang hanya dapat turun membuat level terasa searah, dan menjadi
    masalah besar apabila tujuannya berada di atas.
    """
    terbaik = None
    for lain in daftar_pijakan:
        if lain[1] >= petak[1]:
            continue                    # tidak lebih tinggi
        if bila_terhalang(dinding, petak, lain):
            continue
        if bisa_menyeberang(lain[0] - petak[0], lain[1] - petak[1]):
            if terbaik is None or lain[1] < terbaik[1]:
                terbaik = lain
    return terbaik


def periksa_arah(peta: tuple, dinding: set, daftar_pijakan: list) -> list:
    """Daftar pijakan yang tidak memiliki jalan ke atas."""
    return [petak for petak in daftar_pijakan
            if jalan_ke_atas(peta, dinding, daftar_pijakan, petak) is None]


def kekurangan_terdekat(dinding: set, daftar_pijakan: list,
                        terjebak: list) -> tuple:
    """Mencari jalan keluar terdekat dari daerah terjebak.

    Dikembalikan (jarak diperlukan, jangkauan tersedia, kekurangan, asal,
    tujuan), yaitu lompatan yang paling sedikit kekurangannya. Angka itu
    memberi tahu Anda seberapa jauh perbaikan yang diperlukan.
    """
    terbaik = None
    for petak in terjebak:
        for lain in daftar_pijakan:
            if lain in terjebak or bila_terhalang(dinding, petak, lain):
                continue
            jangkauan = jangkauan_mendatar((petak[1] - lain[1]) * UKURAN_PETAK)
            if jangkauan < 0:
                continue
            jarak = abs(lain[0] - petak[0]) * UKURAN_PETAK
            kekurangan = jarak - jangkauan
            if terbaik is None or kekurangan < terbaik[2]:
                terbaik = (jarak, jangkauan, kekurangan, petak, lain)
    return terbaik


def simulasi(peta: tuple, dinding: set, daftar_pijakan: list, tujuan: tuple,
             banyak: int, acak: random.Random) -> dict:
    """Menjalankan permainan tanpa pemain: titik awalnya diacak berulang
    kali, lalu dihitung berapa yang berhasil mencapai tujuan.

    Cara ini sama gagasannya dengan membiarkan komputer bermain melawan
    dirinya sendiri, yaitu menjalankan permainan berkali-kali tanpa
    menunggu masukan manusia.
    """
    berhasil = 0
    panjang = []
    for _ in range(banyak):
        awal = acak.choice(daftar_pijakan)
        hasil = cari_jalur(peta, dinding, daftar_pijakan, awal, tujuan)
        if hasil["jalur"] is not None:
            berhasil += 1
            panjang.append(len(hasil["jalur"]))
    return {"berhasil": berhasil, "banyak": banyak, "panjang": panjang}


# ---------------------------------------------------------------- Keluaran
def garis(judul: str) -> None:
    print()
    print(judul)
    print("-" * len(judul))


def laporkan(args: argparse.Namespace) -> int:
    nama = args.peta
    peta = PETA[nama]
    dinding, awal, tujuan = baca_peta(peta)
    daftar_pijakan = pijakan(peta, dinding)

    print("=" * 68)
    print(" UJI MANDIRI LEVEL  (tanpa pemain)")
    print("=" * 68)
    print(f" Peta            : {nama}  ({len(peta[0])} x {len(peta)} petak)")
    print(f" Tempat berdiri  : {len(daftar_pijakan)}")
    print(f" Tinggi lompat   : {tinggi_maksimum() / UKURAN_PETAK:.2f} petak")
    print(f" Jarak mendatar  : "
          f"{jangkauan_mendatar(0.0) / UKURAN_PETAK:.2f} petak "
          f"(pada ketinggian yang sama)")

    garis("1. KETERJANGKAUAN")
    terjebak = periksa_keterjangkauan(peta, dinding, daftar_pijakan, tujuan)
    if not terjebak:
        print(" LULUS: seluruh tempat berdiri dapat mencapai tujuan.")
    else:
        persen = round(100 * len(terjebak) / len(daftar_pijakan), 1)
        print(f" GAGAL: {len(terjebak)} dari {len(daftar_pijakan)} tempat "
              f"berdiri ({persen}%) tidak dapat mencapai tujuan.")
        print(" Ini calon soft-lock: pemain yang terlanjur sampai ke sana")
        print(" tidak dapat melanjutkan permainan, walaupun programnya tidak")
        print(" berhenti dan tidak ada pesan kesalahan apa pun.")
        for petak in terjebak[:6]:
            print(f"   terjebak di petak {petak}")
        if len(terjebak) > 6:
            print(f"   ... dan {len(terjebak) - 6} petak lainnya")

        terbaik = kekurangan_terdekat(dinding, daftar_pijakan, terjebak)
        if terbaik is None:
            print(" Seluruh jalan keluar dari daerah terjebak terhalang")
            print(" dinding, sehingga tidak ada lompatan yang dapat diperiksa.")
        else:
            jarak, jangkauan, kurang, dari, ke = terbaik
            print(f" Jalan keluar terdekat: dari {dari} ke {ke}.")
            print(f" Diperlukan jarak {jarak / UKURAN_PETAK:.2f} petak, "
                  f"sedangkan jangkauannya hanya "
                  f"{jangkauan / UKURAN_PETAK:.2f} petak,")
            print(f" yaitu kurang {kurang / UKURAN_PETAK:.2f} petak. "
                  f"Perbaikan sekecil itu sudah cukup.")

    garis("2. JALAN KE ATAS")
    # Tempat yang letaknya sudah tidak lebih rendah daripada tujuan tidak
    # perlu jalan ke atas; yang perlu diperiksa adalah tempat di bawahnya.
    semua_tanpa_naik = periksa_arah(peta, dinding, daftar_pijakan)
    wajar = [p for p in semua_tanpa_naik if p[1] <= tujuan[1]]
    perlu = [p for p in semua_tanpa_naik if p[1] > tujuan[1]]
    print(f" Tanpa jalan ke atas: {len(semua_tanpa_naik)} dari "
          f"{len(daftar_pijakan)} tempat berdiri.")
    print(f"   {len(wajar)} di antaranya setinggi atau lebih tinggi daripada")
    print("   tujuan, sehingga tidak perlu naik. Ini wajar.")
    if not perlu:
        print(" LULUS: tidak ada tempat di bawah tujuan yang hanya dapat turun.")
    else:
        persen = round(100 * len(perlu) / len(daftar_pijakan), 1)
        print(f" PERIKSA: {len(perlu)} tempat ({persen}%) berada di bawah "
              f"tujuan tetapi")
        print(" tidak dapat naik kembali. Pemain yang terjatuh ke sana harus")
        print(" mengulang dari awal, walaupun tujuannya masih dapat dicapai")
        print(" dengan jalan lain.")
        for petak in perlu[:6]:
            print(f"   hanya dapat turun di petak {petak}")
        if len(perlu) > 6:
            print(f"   ... dan {len(perlu) - 6} petak lainnya")

    garis("3. SIMULASI TANPA PEMAIN")
    acak = random.Random(args.benih)
    hasil = simulasi(peta, dinding, daftar_pijakan, tujuan,
                     args.iterasi, acak)
    persen = round(100 * hasil["berhasil"] / hasil["banyak"], 1)
    print(f" Titik awal diacak {hasil['banyak']} kali.")
    print(f" Berhasil mencapai tujuan: {hasil['berhasil']} "
          f"({persen}%).")
    if hasil["panjang"]:
        print(f" Panjang jalur  : terpendek {min(hasil['panjang'])} pijakan, "
              f"terpanjang {max(hasil['panjang'])} pijakan, "
              f"rata-rata {statistics.mean(hasil['panjang']):.1f} pijakan.")

    garis("KESIMPULAN")
    if not terjebak and not perlu:
        print(" Level lolos seluruh pemeriksaan otomatis.")
        print(" Langkah berikutnya adalah playtest dengan pemain, bukan")
        print(" pemeriksaan otomatis. Yang dapat diperiksa mesin hanyalah")
        print(" apakah levelnya mungkin diselesaikan, bukan apakah levelnya")
        print(" menyenangkan.")
        return 0
    print(" Level belum lolos. Perbaiki dahulu daerah yang terjebak dan")
    print(" jalan yang hanya menurun, baru lakukan playtest dengan pemain.")
    return 1


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(
        description="Memeriksa sebuah level platformer tanpa pemain.")
    parser.add_argument("--peta", default="rapi", choices=sorted(PETA),
                        help="nama peta yang diperiksa")
    parser.add_argument("--iterasi", type=int, default=200,
                        help="banyak titik awal yang diacak")
    parser.add_argument("--benih", type=int, default=2025,
                        help="benih pengacakan, supaya hasilnya dapat diulang")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    if args.iterasi < 1:
        print("--iterasi harus bernilai sekurang-kurangnya 1.")
        return 2
    return laporkan(args)


if __name__ == "__main__":
    sys.exit(main())

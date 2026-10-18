"""Pencarian jalur A* pada peta berpetak, beserta visualisasinya.

Program ini memuat peta berpetak yang tersusun dari dinding dan ruang kosong,
lalu mencari jalur terpendek dari titik awal menuju titik tujuan. Pencarian
diperlihatkan langkah demi langkah: petak yang sedang diperiksa, petak yang
menunggu diperiksa, dan jalur yang akhirnya ditemukan.

Tiga pilihan heuristik disediakan untuk dibandingkan:
    manhattan  jarak mendatar ditambah jarak tegak
    euclidean  jarak garis lurus
    tanpa      tanpa perkiraan, sehingga pencarian menjadi algoritma Dijkstra

Pemakaian:
    python ch10_astar.py
    python ch10_astar.py --heuristic euclidean
    python ch10_astar.py --heuristic tanpa
    python ch10_astar.py --frames 400 --auto-close     (uji tanpa jendela)
    python ch10_astar.py --bandingkan                  (bandingkan tiga heuristik)
    python ch10_astar.py --simpan-gambar hasil.png     (simpan tangkapan layar)
"""

from __future__ import annotations

import argparse
import heapq
import math
import sys

import pygame

# ---------------------------------------------------------------- Peta
# '#' dinding, '.' ruang kosong, 'S' titik awal, 'G' titik tujuan.
PETA = (
    "################################",
    "#S...#.........#........#......#",
    "#....#.........#........#......#",
    "#....#....#....#....#...#......#",
    "#....#....#.........#...#......#",
    "#....#....#....#....#...#......#",
    "#..........#....#..............#",
    "#....######.#....#....########.#",
    "#.........#...........#........#",
    "#....#....#....#####..#....#...#",
    "#....#.........#...#.......#...#",
    "#....#....######...#...#...#...#",
    "#....#.............#...#...#...#",
    "#....#############.#...#...#...#",
    "#..................#.......#...#",
    "#....#....#....#...#...#...#...#",
    "#....#....#....#.......#.......#",
    "#....#....#....#...#...#...#...#",
    "#..................#...#......G#",
    "################################",
)

CELL = 28

BACKGROUND_COLOR = (14, 18, 28)
WALL_COLOR = (78, 84, 98)
GRID_COLOR = (34, 42, 58)
START_COLOR = (60, 160, 110)
GOAL_COLOR = (200, 72, 62)
OPEN_COLOR = (22, 28, 42)
FRONTIER_COLOR = (62, 108, 186)
VISITED_COLOR = (38, 54, 80)
CURRENT_COLOR = (240, 190, 70)
PATH_COLOR = (255, 232, 120)
TEXT_COLOR = (235, 240, 250)
HINT_COLOR = (150, 165, 190)

HEURISTICS = ("manhattan", "euclidean", "tanpa")


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Pencarian jalur A* pada peta berpetak")
    parser.add_argument("--heuristic", choices=HEURISTICS, default="manhattan",
                        help="heuristik yang dipakai")
    parser.add_argument("--langkah", type=int, default=2, metavar="N",
                        help="banyaknya petak yang diperiksa setiap bingkai")
    parser.add_argument("--fps", type=int, default=60,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--bandingkan", action="store_true",
                        help="bandingkan ketiga heuristik lalu berhenti")
    parser.add_argument("--simpan-gambar", default="", metavar="BERKAS",
                        help="simpan tangkapan layar sebelum program berakhir")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


# ------------------------------------------------------- Peta dan tetangga
def baca_peta(peta: tuple[str, ...]) -> tuple[set, tuple, tuple]:
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


def tetangga(peta_lebar: int, peta_tinggi: int, dinding: set,
             petak: tuple) -> list[tuple]:
    """Mengembalikan petak-petak yang bersebelahan dan dapat dilalui.

    Hanya empat arah yang dipakai, yaitu atas, bawah, kiri, dan kanan.
    """
    kolom, baris = petak
    hasil = []
    for geser_kolom, geser_baris in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        baru = (kolom + geser_kolom, baris + geser_baris)
        if not (0 <= baru[0] < peta_lebar and 0 <= baru[1] < peta_tinggi):
            continue
        if baru in dinding:
            continue
        hasil.append(baru)
    return hasil


# ------------------------------------------------------------- Heuristik
def jarak_manhattan(a: tuple, b: tuple) -> float:
    """Jarak mendatar ditambah jarak tegak."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def jarak_euclidean(a: tuple, b: tuple) -> float:
    """Jarak garis lurus antara dua petak."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def tanpa_perkiraan(a: tuple, b: tuple) -> float:
    """Tidak ada perkiraan, sehingga pencarian menjadi algoritma Dijkstra."""
    return 0.0


HEURISTIC_FUNCTIONS = {
    "manhattan": jarak_manhattan,
    "euclidean": jarak_euclidean,
    "tanpa": tanpa_perkiraan,
}


# ---------------------------------------------------------------- A*
def cari_jalur(peta: tuple[str, ...], awal: tuple, tujuan: tuple,
               nama_heuristik: str, batas: int = 0) -> dict:
    """Mencari jalur terpendek dengan algoritma A*.

    Mengembalikan kamus yang memuat jalur, banyaknya petak yang diperiksa,
    biaya jalur, serta urutan pemeriksaan dan daftar tepi pencarian untuk
    keperluan penggambaran.
    """
    dinding, _, _ = baca_peta(peta)
    lebar, tinggi = len(peta[0]), len(peta)
    heuristik = HEURISTIC_FUNCTIONS[nama_heuristik]

    # Tepi pencarian berupa antrean prioritas. Isinya pasangan
    # (perkiraan biaya total, biaya sejauh ini, petak).
    tepi: list[tuple[float, int, tuple]] = [(heuristik(awal, tujuan), 0, awal)]
    asal = {awal: None}
    biaya = {awal: 0}

    urutan_diperiksa: list[tuple] = []
    urutan_tepi: list[list[tuple]] = []

    while tepi:
        _, biaya_sekarang, sekarang = heapq.heappop(tepi)
        if biaya_sekarang > biaya.get(sekarang, 0):
            continue                       # sisa lama, lewati
        urutan_diperiksa.append(sekarang)
        urutan_tepi.append([petak for _, _, petak in tepi])

        if sekarang == tujuan:
            break
        if batas and len(urutan_diperiksa) >= batas:
            break

        for tetangga_petak in tetangga(lebar, tinggi, dinding, sekarang):
            biaya_baru = biaya_sekarang + 1
            if tetangga_petak not in biaya or biaya_baru < biaya[tetangga_petak]:
                biaya[tetangga_petak] = biaya_baru
                perkiraan = biaya_baru + heuristik(tetangga_petak, tujuan)
                heapq.heappush(tepi, (perkiraan, biaya_baru, tetangga_petak))
                asal[tetangga_petak] = sekarang

    # Rekonstruksi jalur dengan menelusuri kembali asal setiap petak.
    jalur: list[tuple] = []
    if tujuan in asal:
        petak = tujuan
        while petak is not None:
            jalur.append(petak)
            petak = asal[petak]
        jalur.reverse()

    return {
        "jalur": jalur,
        "diperiksa": urutan_diperiksa,
        "tepi": urutan_tepi,
        "biaya": biaya.get(tujuan, 0),
        "heuristik": nama_heuristik,
    }


def periksa_jalur(peta: tuple[str, ...], awal: tuple, tujuan: tuple,
                  jalur: list[tuple]) -> list[str]:
    """Memeriksa keabsahan jalur dan mengembalikan daftar temuan."""
    temuan: list[str] = []
    dinding, _, _ = baca_peta(peta)

    if not jalur:
        temuan.append("jalur kosong: tujuan tidak dapat dicapai")
        return temuan
    if jalur[0] != awal:
        temuan.append(f"jalur tidak dimulai dari titik awal: {jalur[0]}")
    if jalur[-1] != tujuan:
        temuan.append(f"jalur tidak berakhir di titik tujuan: {jalur[-1]}")

    for petak in jalur:
        if petak in dinding:
            temuan.append(f"jalur melewati dinding pada petak {petak}")
    for sebelum, sesudah in zip(jalur, jalur[1:]):
        if jarak_manhattan(sebelum, sesudah) != 1:
            temuan.append(
                f"jalur melompat dari {sebelum} ke {sesudah}")
    return temuan


# ------------------------------------------------------------ Penggambaran
def gambar_peta(pygame, screen, peta: tuple[str, ...], hasil: dict,
                langkah: int, font) -> None:
    """Menggambar peta, keadaan pencarian, dan jalur yang ditemukan."""
    dinding, awal, tujuan = baca_peta(peta)
    lebar, tinggi = len(peta[0]), len(peta)

    screen.fill(BACKGROUND_COLOR)

    diperiksa = hasil["diperiksa"][:langkah]
    himpunan_diperiksa = set(diperiksa)

    if langkah <= len(hasil["tepi"]) and hasil["tepi"]:
        tepi_kini = set(hasil["tepi"][min(langkah, len(hasil["tepi"])) - 1])
    else:
        tepi_kini = set()

    for baris in range(tinggi):
        for kolom in range(lebar):
            petak = (kolom, baris)
            kotak = pygame.Rect(kolom * CELL, baris * CELL, CELL, CELL)
            if petak in dinding:
                pygame.draw.rect(screen, WALL_COLOR, kotak)
            else:
                pygame.draw.rect(screen, OPEN_COLOR, kotak)

            if petak in himpunan_diperiksa:
                pygame.draw.rect(screen, VISITED_COLOR, kotak)
            elif petak in tepi_kini:
                pygame.draw.rect(screen, FRONTIER_COLOR, kotak)

            pygame.draw.rect(screen, GRID_COLOR, kotak, 1)

    # Jalur hasil pencarian.
    if hasil["jalur"] and langkah >= len(hasil["diperiksa"]):
        for petak in hasil["jalur"]:
            pusat = (petak[0] * CELL + CELL // 2, petak[1] * CELL + CELL // 2)
            pygame.draw.circle(screen, PATH_COLOR, pusat, CELL // 6)

    # Petak yang sedang diperiksa.
    if diperiksa:
        kolom, baris = diperiksa[-1]
        pygame.draw.rect(screen, CURRENT_COLOR,
                         pygame.Rect(kolom * CELL, baris * CELL, CELL, CELL), 2)

    # Titik awal dan titik tujuan.
    for petak, warna in ((awal, START_COLOR), (tujuan, GOAL_COLOR)):
        pygame.draw.rect(screen, warna,
                         pygame.Rect(petak[0] * CELL, petak[1] * CELL,
                                     CELL, CELL), 3)

    baris_teks = [
        f"Heuristik        : {hasil['heuristik']}",
        f"Petak diperiksa  : {min(langkah, len(hasil['diperiksa']))} "
        f"dari {len(hasil['diperiksa'])}",
        f"Panjang jalur     : {len(hasil['jalur'])} petak",
        f"Biaya jalur       : {hasil['biaya']}",
    ]
    y = tinggi * CELL + 8
    for teks in baris_teks:
        screen.blit(font.render(teks, True, TEXT_COLOR), (10, y))
        y += 20

    petunjuk = font.render(
        "Tekan ESC untuk keluar   R untuk mengulang   H untuk ganti heuristik",
        True, HINT_COLOR)
    screen.blit(petunjuk, (10, y))


def jalankan_pencarian(args) -> dict:
    """Menjalankan pencarian dan menampilkan hasilnya pada terminal."""
    dinding, awal, tujuan = baca_peta(PETA)
    hasil = cari_jalur(PETA, awal, tujuan, args.heuristic)

    temuan = periksa_jalur(PETA, awal, tujuan, hasil["jalur"])
    print(f"Heuristik          : {hasil['heuristik']}")
    print(f"Petak diperiksa    : {len(hasil['diperiksa'])}")
    print(f"Panjang jalur      : {len(hasil['jalur'])} petak")
    print(f"Biaya jalur        : {hasil['biaya']}")
    if temuan:
        for satu in temuan:
            print(f"  ! {satu}")
        print("Hasil pemeriksaan  : JALUR TIDAK SAH")
    else:
        print("Hasil pemeriksaan  : jalur sah, tidak melewati dinding")
    return hasil


def main() -> int:
    args = parse_arguments()

    if args.bandingkan:
        hasil_semua = []
        for nama in HEURISTICS:
            hasil = cari_jalur(PETA, *baca_peta(PETA)[1:], nama)
            temuan = periksa_jalur(PETA, *baca_peta(PETA)[1:], hasil["jalur"])
            hasil_semua.append((nama, len(hasil["diperiksa"]),
                                len(hasil["jalur"]), hasil["biaya"],
                                len(temuan)))
        print("=" * 62)
        print(" PERBANDINGAN HEURISTIK")
        print("=" * 62)
        print(f"{'Heuristik':>11} {'Diperiksa':>10} {'Jalur':>7} "
              f"{'Biaya':>7} {'Temuan':>7}")
        print("-" * 62)
        for nama, diperiksa, panjang, biaya, temuan in hasil_semua:
            print(f"{nama:>11} {diperiksa:>10} {panjang:>7} "
                  f"{biaya:>7} {temuan:>7}")
        print("-" * 62)
        biaya_semua = {biaya for _, _, _, biaya, _ in hasil_semua}
        if len(biaya_semua) == 1:
            print("Biaya jalur sama pada ketiga heuristik, "
                  "sehingga ketiganya menghasilkan jalur terpendek.")
        else:
            print("Biaya jalur berbeda, sehingga ada heuristik yang "
                  "tidak menghasilkan jalur terpendek.")
        return 0

    pygame.init()
    lebar, tinggi = len(PETA[0]), len(PETA)
    screen = pygame.display.set_mode((lebar * CELL, tinggi * CELL + 100))
    pygame.display.set_caption("Bab X - pencarian jalur A*")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    hasil = jalankan_pencarian(args)
    langkah = 0
    jumlah_langkah = len(hasil["diperiksa"])
    running = True

    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    langkah = 0
                elif event.key == pygame.K_h:
                    nomor = HEURISTICS.index(args.heuristic)
                    args.heuristic = HEURISTICS[(nomor + 1) % len(HEURISTICS)]
                    hasil = jalankan_pencarian(args)
                    jumlah_langkah = len(hasil["diperiksa"])
                    langkah = 0

        langkah = min(jumlah_langkah, langkah + args.langkah)

        gambar_peta(pygame, screen, PETA, hasil, langkah, font)
        pygame.display.flip()
        clock.tick(args.fps)

        if args.frames and langkah >= jumlah_langkah:
            running = False

    if args.simpan_gambar:
        pygame.image.save(screen, args.simpan_gambar)
        print(f"Tangkapan layar disimpan pada {args.simpan_gambar}")

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())

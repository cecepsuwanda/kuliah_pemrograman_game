"""Mini proyek AI: mesin keadaan yang memanggil pencarian jalur.

Program ini menggabungkan dua bab sebelumnya. Setiap NPC memiliki mesin keadaan
(berpatroli dan mengejar), dan ketika berada pada keadaan mengejar ia memanggil
pencarian jalur A* untuk menentukan rutenya. Pencarian itu tidak dijalankan
setiap bingkai, melainkan menurut selang waktu yang dapat diatur.

Pemain bergerak bebas dengan tombol dan tidak dapat melewati dinding. Program
mencatat tiga besaran untuk keperluan penilaian mutu perilaku:
    banyaknya pencarian jalur yang dijalankan
    banyaknya petak yang diperiksa pencarian
    rata-rata jarak NPC terhadap pemain selama permainan

Pengendalian:
    W A S D atau tombol panah : menggerakkan pemain
    ESC                       : mengakhiri program

Pemakaian:
    python ch11_mini_proyek.py
    python ch11_mini_proyek.py --npc 4 --repath 0.4
    python ch11_mini_proyek.py --frames 600 --auto-run     (uji tanpa jendela)
    python ch11_mini_proyek.py --evaluasi                   (bandingkan selang)
"""

from __future__ import annotations

import argparse
import math
import sys

import pygame

# Pencarian jalur diambil dari berkas bab sebelumnya, bukan ditulis ulang.
import ch10_astar as pencarian

BACKGROUND_COLOR = (16, 20, 30)
WALL_COLOR = (74, 80, 94)
FLOOR_COLOR = (26, 32, 46)
PLAYER_COLOR = (46, 117, 182)
NPC_PATROL_COLOR = (70, 150, 110)
NPC_CHASE_COLOR = (190, 74, 66)
PATH_COLOR = (240, 210, 110)
TEXT_COLOR = (235, 240, 250)
HINT_COLOR = (150, 165, 190)

CELL = pencarian.CELL
PLAYER_SIZE = 22
NPC_SIZE = 24

PLAYER_SPEED = 210.0
PATROL_SPEED = 80.0
CHASE_SPEED = 165.0
PERCEPTION_CELLS = 7.0
REACH_DISTANCE = 5.0

DEFAULT_NPC = 3
DEFAULT_REPATH = 0.3
DEFAULT_FPS = 60

# Titik patroli, dinyatakan dalam petak.
PATROL_POINTS = ((3, 17), (9, 17), (9, 11), (3, 11))


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Mini proyek AI: FSM dan A*")
    parser.add_argument("--npc", type=int, default=DEFAULT_NPC,
                        help="banyaknya NPC")
    parser.add_argument("--repath", type=float, default=DEFAULT_REPATH,
                        help="selang waktu menghitung ulang jalur, dalam detik")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-run", action="store_true",
                        help="gerakkan pemain secara otomatis untuk pengujian")
    parser.add_argument("--evaluasi", action="store_true",
                        help="bandingkan beberapa selang hitung ulang lalu berhenti")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


def pusat_petak(petak: tuple) -> pygame.Vector2:
    """Mengembalikan titik tengah sebuah petak dalam piksel."""
    return pygame.Vector2(petak[0] * CELL + CELL / 2,
                          petak[1] * CELL + CELL / 2)


def petak_dari_piksel(posisi: pygame.Vector2) -> tuple:
    """Mengembalikan petak yang memuat sebuah titik."""
    return (int(posisi.x // CELL), int(posisi.y // CELL))


class Player(pygame.sprite.Sprite):
    """Pemain yang bergerak bebas dan tidak dapat melewati dinding."""

    def __init__(self, petak: tuple) -> None:
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.position = pusat_petak(petak)
        self.rect = self.image.get_rect(center=(round(self.position.x),
                                                round(self.position.y)))

    def update(self, delta_seconds: float, direction, dinding) -> None:
        """Memperbarui gerak pemain, menolak perpindahan ke dalam dinding."""
        if direction.length_squared() > 0:
            velocity = direction.normalize() * PLAYER_SPEED
        else:
            velocity = pygame.Vector2(0, 0)

        baru = self.position + velocity * delta_seconds
        if petak_dari_piksel(baru) not in dinding:
            self.position = baru
        self.rect.center = (round(self.position.x), round(self.position.y))


class Npc(pygame.sprite.Sprite):
    """NPC bermesin keadaan yang memanggil pencarian jalur ketika mengejar."""

    def __init__(self, petak: tuple, index: int, selang: float,
                 statistik: dict) -> None:
        super().__init__()
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.image.fill(NPC_PATROL_COLOR)
        self.position = pusat_petak(petak)
        self.rect = self.image.get_rect(center=(round(self.position.x),
                                                round(self.position.y)))
        self.state = "berpatroli"
        self.index = index
        self.selang = selang
        self.statistik = statistik
        self.jalur: list[tuple] = []
        self.selang_tersisa = 0.0
        self.frames = 0
        self.jarak = 0.0

    def petak_sekarang(self) -> tuple:
        """Petak tempat NPC berada sekarang."""
        return petak_dari_piksel(self.position)

    def hitung_jalur(self, tujuan: tuple) -> None:
        """Memanggil pencarian jalur dan mencatat biayanya."""
        hasil = pencarian.cari_jalur(pencarian.PETA, self.petak_sekarang(),
                                     tujuan, "manhattan")
        self.jalur = hasil["jalur"][1:]        # petak pertama adalah petak sendiri
        self.statistik["hitung_ulang"] += 1
        self.statistik["petak_diperiksa"] += len(hasil["diperiksa"])

    def update(self, delta_seconds: float, pemain: Player, dinding: set) -> None:
        """Menjalankan mesin keadaan, pencarian jalur, dan gerak."""
        self.frames += 1
        to_player = pemain.position - self.position
        self.jarak = to_player.length()
        jauh_petak = self.jarak / CELL

        # ---------- Mesin keadaan ----------
        if self.state == "berpatroli":
            if jauh_petak <= PERCEPTION_CELLS:
                self.state = "mengejar"
                self.selang_tersisa = 0.0
        elif self.state == "mengejar":
            if jauh_petak > PERCEPTION_CELLS * 1.4:
                self.state = "berpatroli"
                self.jalur = []
        self.image.fill(NPC_CHASE_COLOR if self.state == "mengejar"
                        else NPC_PATROL_COLOR)

        # ---------- Tindakan ----------
        if self.state == "mengejar":
            self.selang_tersisa -= delta_seconds
            if self.selang_tersisa <= 0.0 or not self.jalur:
                self.hitung_jalur(petak_dari_piksel(pemain.position))
                self.selang_tersisa = self.selang
            self.ikuti_jalur(delta_seconds, CHASE_SPEED, dinding)
        else:
            self.berpatroli(delta_seconds, dinding)

    def ikuti_jalur(self, delta_seconds: float, kecepatan: float,
                    dinding: set) -> None:
        """Bergerak menuju titik tengah petak berikutnya pada jalur."""
        while self.jalur:
            tujuan = pusat_petak(self.jalur[0])
            arah = tujuan - self.position
            if arah.length() <= REACH_DISTANCE:
                self.jalur.pop(0)
                continue
            self.position += arah.normalize() * kecepatan * delta_seconds
            break
        self.rect.center = (round(self.position.x), round(self.position.y))

    def berpatroli(self, delta_seconds: float, dinding: set) -> None:
        """Bergerak lurus menuju titik patroli berikutnya."""
        tujuan_petak = PATROL_POINTS[self.index % len(PATROL_POINTS)]
        tujuan = pusat_petak(tujuan_petak)
        arah = tujuan - self.position
        if arah.length() <= REACH_DISTANCE:
            self.index += 1
            return
        self.position += arah.normalize() * PATROL_SPEED * delta_seconds
        self.rect.center = (round(self.position.x), round(self.position.y))


def skenario_pemain(frames: int, fps: int) -> tuple:
    """Jalur pemain yang tetap, dipakai untuk membandingkan selang hitung ulang.

    Pemain bergerak menyusuri lorong bolak-balik, sehingga NPC harus menghitung
    ulang jalurnya berkali-kali.
    """
    langkah = (frames / fps) % 8.0
    if langkah < 4.0:
        kolom = 2.0 + langkah * 3.5
    else:
        kolom = 16.0 - (langkah - 4.0) * 3.5
    return (kolom * CELL + CELL / 2, 17 * CELL + CELL / 2)


def jalankan_evaluasi(npc_jumlah: int, selang_semua: tuple, frames: int,
                       fps: int) -> None:
    """Menjalankan permainan beberapa kali dengan selang berbeda, lalu membandingkan."""
    print("=" * 74)
    print(" EVALUASI SELANG WAKTU MENGHITUNG ULANG JALUR")
    print(f" {npc_jumlah} NPC, {frames} bingkai pada {fps} bingkai per detik")
    print("=" * 74)
    print()
    print(f"{'Selang':>8} {'Hitung ulang':>14} {'Petak diperiksa':>18} "
          f"{'Jarak akhir':>13} {'Jarak rata-rata':>16}")
    print("-" * 74)

    for selang in selang_semua:
        dinding, _, _ = pencarian.baca_peta(pencarian.PETA)
        statistik = {"hitung_ulang": 0, "petak_diperiksa": 0}
        pemain = Player((2, 17))
        npcs = [Npc((3, 17), i, selang, statistik) for i in range(npc_jumlah)]

        total_jarak = 0.0
        for nomor in range(frames):
            pemain.position = pygame.Vector2(*skenario_pemain(nomor, fps))
            pemain.rect.center = (round(pemain.position.x),
                                   round(pemain.position.y))
            for npc in npcs:
                npc.update(1.0 / fps, pemain, dinding)
            total_jarak += sum(npc.jarak for npc in npcs) / len(npcs)

        jarak_akhir = sum(npc.jarak for npc in npcs) / len(npcs)
        print(f"{selang:>7.2f}s {statistik['hitung_ulang']:>14} "
              f"{statistik['petak_diperiksa']:>18} "
              f"{jarak_akhir:>10.0f} px {total_jarak / frames:>13.0f} px")

    print("-" * 74)
    print()
    print("Catatan: jarak dinyatakan dalam piksel. Jarak yang lebih kecil")
    print("menandakan NPC lebih rapat mendekati pemain, yaitu perilaku yang")
    print("lebih baik, sedangkan angka hitung ulang yang lebih besar menandakan")
    print("beban perhitungan yang lebih berat.")


def main() -> int:
    args = parse_arguments()

    if args.evaluasi:
        jalankan_evaluasi(args.npc, (0.0, 0.15, 0.3, 0.6, 1.2), 900, args.fps)
        return 0

    pygame.init()
    lebar = len(pencarian.PETA[0]) * CELL
    tinggi = len(pencarian.PETA) * CELL
    screen = pygame.display.set_mode((lebar, tinggi + 64))
    pygame.display.set_caption("Bab XI - mini proyek AI")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)

    dinding, _, _ = pencarian.baca_peta(pencarian.PETA)
    statistik = {"hitung_ulang": 0, "petak_diperiksa": 0}
    pemain = Player((2, 17))
    npcs = [Npc((3, 17), i, args.repath, statistik) for i in range(args.npc)]

    frames = 0
    total_jarak = 0.0
    delta_seconds = 0.0
    running = True

    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        # ---------- Tahap 1: membaca masukan ----------
        direction = pygame.Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        if args.auto_run:
            pemain.position = pygame.Vector2(*skenario_pemain(frames, args.fps))
            pemain.rect.center = (round(pemain.position.x),
                                   round(pemain.position.y))
        else:
            pemain.update(delta_seconds, direction, dinding)

        # ---------- Tahap 2: memperbarui keadaan ----------
        for npc in npcs:
            npc.update(delta_seconds, pemain, dinding)
        total_jarak += sum(npc.jarak for npc in npcs) / len(npcs)

        frames += 1
        measured_fps = clock.get_fps()

        # ---------- Tahap 3: menayangkan ----------
        screen.fill(BACKGROUND_COLOR)
        for baris in range(len(pencarian.PETA)):
            for kolom in range(len(pencarian.PETA[0])):
                kotak = pygame.Rect(kolom * CELL, baris * CELL, CELL, CELL)
                warna = (WALL_COLOR if (kolom, baris) in dinding
                         else FLOOR_COLOR)
                pygame.draw.rect(screen, warna, kotak)

        for npc in npcs:
            for petak in npc.jalur:
                pygame.draw.circle(screen, PATH_COLOR, pusat_petak(petak), 2)

        for npc in npcs:
            screen.blit(npc.image, npc.rect)
        screen.blit(pemain.image, pemain.rect)

        baris_teks = [
            f"Bingkai            : {frames:5d}",
            f"Laju bingkai       : {measured_fps:5.1f} FPS",
            f"Selang hitung ulang: {args.repath:.2f} detik",
            f"Hitung ulang jalur : {statistik['hitung_ulang']}",
            f"Petak diperiksa    : {statistik['petak_diperiksa']}",
            f"Jarak rata-rata    : {total_jarak / max(1, frames):5.0f} piksel",
        ]
        y = tinggi + 6
        for teks in baris_teks:
            screen.blit(font.render(teks, True, TEXT_COLOR), (8, y))
            y += 19

        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frames >= args.frames:
            running = False

    pygame.quit()

    print(f"Bingkai dijalankan : {frames}")
    print(f"Selang hitung ulang: {args.repath:.2f} detik")
    print(f"Hitung ulang jalur : {statistik['hitung_ulang']}")
    print(f"Petak diperiksa    : {statistik['petak_diperiksa']}")
    print(f"Jarak rata-rata    : {total_jarak / max(1, frames):.0f} piksel")
    return 0


if __name__ == "__main__":
    sys.exit(main())

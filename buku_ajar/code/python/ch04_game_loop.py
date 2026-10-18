"""Siklus permainan lengkap: masukan, pembaruan, dan penayangan.

Berbeda dari program pada Bab III, program ini menjalankan siklus yang
sesungguhnya: ketiga tahap dikerjakan berulang kali tanpa berhenti sampai
jendela ditutup.

Pengendalian:
    tutup jendela atau ESC : mengakhiri program
    panah atas             : menaikkan batas laju bingkai
    panah bawah            : menurunkan batas laju bingkai
    spasi                  : mengembalikan penghitung bingkai ke nol

Pemakaian:
    python ch04_game_loop.py
    python ch04_game_loop.py --fps 30
    python ch04_game_loop.py --fps 0            (tanpa pembatasan laju)
    python ch04_game_loop.py --frames 120       (uji tanpa jendela)
    python ch04_game_loop.py --auto-close       (keluar setelah satu bingkai)
"""

from __future__ import annotations

import argparse
import sys

BACKGROUND_COLOR = (24, 32, 52)
TEXT_COLOR = (255, 255, 255)
MARKER_COLOR = (46, 117, 182)
HINT_COLOR = (150, 165, 190)

DEFAULT_FPS = 60
FPS_STEP = 15
MIN_FPS = 15
MAX_FPS = 240

# Penanda bahwa siklus berjalan: panjang batang bertambah setiap bingkai lalu
# kembali ke nol setelah melewati nilai ini.
MARKER_PERIOD = 240


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Siklus permainan Pygame")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik; 0 berarti tanpa batas")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian tanpa jendela")
    return parser.parse_args()


def update_state(frame_count: int) -> int:
    """Tahap pembaruan. Mengembalikan nomor bingkai yang baru.

    Pada bab ini keadaan yang diperbarui masih sederhana, yaitu penghitung
    bingkai. Mulai Bab V keadaan yang diperbarui mencakup posisi dan kecepatan
    objek.
    """
    return frame_count + 1


def draw_window(pygame, screen, font, big_font, frame_count: int,
                measured_fps: float, fps_label: str,
                elapsed_seconds: float) -> None:
    """Tahap penayangan. Menggambar seluruh isi jendela dari awal."""
    width, height = screen.get_size()

    screen.fill(BACKGROUND_COLOR)

    title = big_font.render("Siklus Permainan", True, TEXT_COLOR)
    screen.blit(title, (30, 30))

    lines = [
        f"Laju terukur : {measured_fps:8.1f} FPS",
        f"Batas laju   : {fps_label:>8} FPS",
        f"Bingkai ke   : {frame_count:8d}",
        f"Waktu jalan  : {elapsed_seconds:8.1f} detik",
    ]
    y = 90
    for line in lines:
        screen.blit(font.render(line, True, TEXT_COLOR), (30, y))
        y += 28

    max_length = width - 60
    bar_length = int((frame_count % MARKER_PERIOD) / MARKER_PERIOD * max_length)
    pygame.draw.rect(screen, MARKER_COLOR, (30, height - 90, max_length, 14), 1)
    pygame.draw.rect(screen, MARKER_COLOR, (30, height - 90, bar_length, 14))

    hint = font.render(
        "Panah atas/bawah: ubah batas laju   Spasi: nol-kan   ESC: keluar",
        True, HINT_COLOR)
    screen.blit(hint, (30, height - 50))


def main() -> int:
    args = parse_arguments()

    import pygame

    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Bab IV - siklus permainan")

    # Clock dipakai untuk dua hal sekaligus: membatasi laju bingkai dan
    # mengukur selang waktu antar-bingkai.
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    big_font = pygame.font.Font(None, 40)

    # Nilai 0 berarti tanpa pembatasan laju; nilai lain dibatasi agar tetap
    # masuk rentang yang masuk akal.
    fps_limit = args.fps
    if fps_limit != 0:
        fps_limit = max(MIN_FPS, min(MAX_FPS, fps_limit))
    frame_count = 0
    delta_seconds = 0.0
    running = True
    start_ticks = pygame.time.get_ticks()

    # Mode uji tanpa jendela: peristiwa QUIT dikirim program sendiri sehingga
    # perulangan berakhir pada bingkai pertama. Apabila --frames dipakai,
    # perulangan berakhir karena batas bingkai tercapai, jadi QUIT tidak perlu.
    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        # ---------- Tahap 1: membaca masukan ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    # Penekanan pertama setelah mode tanpa batas mengembalikan
                    # program ke batas laju bawaan.
                    if fps_limit == 0:
                        fps_limit = DEFAULT_FPS
                    else:
                        fps_limit = min(MAX_FPS, fps_limit + FPS_STEP)
                elif event.key == pygame.K_DOWN:
                    if fps_limit == 0:
                        fps_limit = MIN_FPS
                    else:
                        fps_limit = max(MIN_FPS, fps_limit - FPS_STEP)
                elif event.key == pygame.K_SPACE:
                    frame_count = 0

        # ---------- Tahap 2: memperbarui keadaan ----------
        frame_count = update_state(frame_count)
        measured_fps = clock.get_fps()
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
        fps_label = "tanpa" if fps_limit == 0 else str(fps_limit)
        pygame.display.set_caption(
            f"Bab IV - siklus permainan | {measured_fps:.1f} FPS "
            f"(batas {fps_label})")

        # ---------- Tahap 3: menayangkan ----------
        draw_window(pygame, screen, font, big_font, frame_count,
                    measured_fps, fps_label, elapsed_seconds)
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        # tick() menunggu sampai selang waktu satu bingkai tercapai sehingga
        # laju tidak melampaui batas, dan mengembalikan selang waktu yang
        # benar-benar berjalan, dalam milidetik.
        delta_seconds = clock.tick(fps_limit) / 1000.0

        if args.frames and frame_count >= args.frames:
            running = False

    # Waktu berakhir dihitung sebelum pygame.quit(), sebab sesudahnya
    # pygame.time.get_ticks() tidak lagi menghitung waktu berjalan.
    total_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
    pygame.quit()

    print(f"Bingkai dijalankan  : {frame_count}")
    print(f"Waktu berjalan      : {total_seconds:.2f} detik")
    print(f"Selang bingkai akhir: {delta_seconds * 1000:.2f} milidetik")
    if total_seconds > 0:
        print(f"Laju rata-rata      : {frame_count / total_seconds:.1f} FPS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Program Pygame pertama: membuka jendela dan menampilkan informasi versi.

Program ini sengaja belum memakai siklus permainan. Ia membuka jendela,
menggambar isinya satu kali, lalu menunggu sampai jendela ditutup. Perulangan
yang ada di dalamnya hanya menunggu peristiwa, belum memperbarui keadaan dan
belum menggambar ulang. Siklus permainan yang sebenarnya dibahas pada Bab IV.

Pemakaian:
    python ch03_jendela.py
    python ch03_jendela.py --width 800 --height 600
    python ch03_jendela.py --auto-close    (pengujian otomatis tanpa jendela)
"""

from __future__ import annotations

import argparse
import sys

# Warna dinyatakan sebagai rangkap tiga nilai merah, hijau, dan biru (0-255).
WARNA_LATAR = (31, 56, 100)
WARNA_TEKS = (255, 255, 255)


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan yang diberikan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Jendela Pygame pertama")
    parser.add_argument("--width", type=int, default=640,
                        help="lebar jendela dalam piksel (bawaan 640)")
    parser.add_argument("--height", type=int, default=480,
                        help="tinggi jendela dalam piksel (bawaan 480)")
    parser.add_argument("--auto-close", action="store_true",
                        help="mengirim sendiri peristiwa QUIT agar dapat diuji tanpa jendela")
    return parser.parse_args()


def build_lines(pygame) -> list[str]:
    """Menyusun baris teks yang akan ditampilkan pada jendela."""
    sdl_version = ".".join(str(part) for part in pygame.get_sdl_version())
    return [
        "Pengantar Pemrograman Game",
        "",
        f"Python    : {sys.version.split()[0]}",
        f"Pygame    : {pygame.version.ver}",
        f"SDL       : {sdl_version}",
        f"Pengandar : {pygame.display.get_driver()}",
        "",
        "Tutup jendela ini untuk mengakhiri program.",
    ]


def main() -> int:
    args = parse_arguments()

    import pygame

    pygame.init()
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption("Bab III - Jendela Pygame pertama")

    # Latar jendela diisi satu warna terlebih dahulu.
    screen.fill(WARNA_LATAR)

    # Huruf bawaan Pygame dipakai agar program tidak bergantung pada huruf
    # yang terpasang pada sistem operasi.
    font = pygame.font.Font(None, 26)
    y = 40
    for line in build_lines(pygame):
        if line:
            image = font.render(line, True, WARNA_TEKS)
            screen.blit(image, (40, y))
        y += 32

    pygame.display.flip()
    print(f"Jendela {args.width}x{args.height} dibuka. "
          f"Tutup jendela untuk mengakhiri program.")

    if args.auto_close:
        # Pengujian otomatis: peristiwa QUIT dikirim oleh program sendiri
        # sehingga perulangan di bawah langsung berakhir.
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Perulangan menunggu peristiwa. Ini belum siklus permainan: keadaan belum
    # diperbarui dan layar belum digambar ulang.
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False

    pygame.quit()
    print("Program selesai. Lingkungan kerja berjalan dengan baik.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

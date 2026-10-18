"""Memeriksa kesiapan lingkungan kerja untuk mata kuliah Pengantar Pemrograman Game.

Skrip ini tidak membuka jendela apa pun, sehingga aman dijalankan pada komputer
tanpa layar, misalnya melalui sesi jarak jauh.

Kode keluar 0 berarti lingkungan siap dipakai. Kode keluar 1 berarti ada bagian
yang perlu diperbaiki lebih dahulu sebelum praktikum dikerjakan.

Pemakaian:
    python ch03_periksa_lingkungan.py
"""

from __future__ import annotations

import platform
import sys

# Versi Python terendah yang dipakai pada buku ini.
MINIMUM_PYTHON = (3, 8)


def check_python() -> bool:
    """Memeriksa versi Python dan menyampaikan lokasi penafsirnya."""
    version = platform.python_version()
    ok = sys.version_info >= MINIMUM_PYTHON
    if ok:
        status = "siap"
    else:
        status = f"perlu {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]} atau lebih baru"

    print(f"Python           : {version} ({status})")
    print(f"Sistem operasi   : {platform.system()} {platform.release()} {platform.machine()}")
    print(f"Penafsir Python  : {sys.executable}")
    return ok


def check_pygame() -> bool:
    """Memeriksa apakah Pygame terpasang dan dapat dipakai."""
    try:
        import pygame
    except ImportError:
        print("Pygame           : belum terpasang")
        print("                   pasang dengan perintah berikut, lalu jalankan ulang:")
        print("                   python -m pip install pygame")
        return False

    print(f"Pygame           : {pygame.version.ver}")
    print(f"SDL              : {'.'.join(str(part) for part in pygame.get_sdl_version())}")

    pygame.init()
    try:
        pygame.display.init()
        print(f"Pengandar video  : {pygame.display.get_driver()}")

        pygame.font.init()
        font = pygame.font.Font(None, 24)
        print(f"Huruf bawaan     : tersedia (tinggi {font.get_height()} piksel)")
    finally:
        pygame.quit()
    return True


def main() -> int:
    print("=" * 60)
    print(" PEMERIKSAAN LINGKUNGAN KERJA")
    print(" Pengantar Pemrograman Game")
    print("=" * 60)
    print()

    results = [check_python(), check_pygame()]

    print()
    if all(results):
        print("Hasil: lingkungan siap dipakai. Lanjutkan ke praktikum.")
        return 0

    print("Hasil: ada bagian yang belum siap.")
    print("Perbaiki lebih dahulu, lalu jalankan ulang skrip ini.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

"""Mengukur pengaruh batas laju bingkai terhadap beban prosesor.

Program ini menjalankan siklus yang sama dengan ch04_game_loop.py, tetapi
tanpa jendela dan untuk jangka waktu yang tetap. Setiap batas laju diuji
bergantian, lalu hasilnya dibandingkan.

Yang diukur:
    frames         banyaknya bingkai yang berhasil diselesaikan
    rate           rata-rata bingkai per detik
    cpu seconds    waktu yang benar-benar dipakai prosesor
    cpu usage      perbandingan waktu prosesor terhadap waktu berjalan

Pemakaian prosesor dihitung dari waktu prosesor dibagi waktu berjalan.
Nilai mendekati 100 persen berarti satu inti prosesor dipakai penuh.

Pemakaian:
    python ch04_ukur_laju.py
    python ch04_ukur_laju.py --caps 30,60,120,0 --duration 2
"""

from __future__ import annotations

import argparse
import sys
import time

BACKGROUND_COLOR = (24, 32, 52)
BOX_COLOR = (46, 117, 182)


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(
        description="Mengukur pengaruh batas laju bingkai")
    parser.add_argument("--caps", default="30,60,120,0",
                        help="daftar batas laju yang diuji; 0 berarti tanpa batas")
    parser.add_argument("--duration", type=float, default=2.0,
                        help="lama setiap pengujian, dalam detik")
    parser.add_argument("--size", default="720x480",
                        help="ukuran permukaan gambar, misalnya 720x480")
    return parser.parse_args()


def run_cycle(pygame, size: tuple[int, int], cap: int,
              duration: float) -> dict[str, float]:
    """Menjalankan satu konfigurasi dan mengembalikan hasil pengukurannya."""
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    frames = 0
    cpu_start = time.process_time()
    wall_start = time.perf_counter()

    running = True
    while running:
        # Siklus yang disederhanakan: masukan, pembaruan, penayangan.
        for _ in pygame.event.get():
            pass

        frames += 1
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, BOX_COLOR, (100, 100, 200, 100))
        pygame.display.flip()

        clock.tick(cap)

        if time.perf_counter() - wall_start >= duration:
            running = False

    cpu_seconds = time.process_time() - cpu_start
    wall_seconds = time.perf_counter() - wall_start

    return {
        "cap": cap,
        "frames": frames,
        "rate": frames / wall_seconds,
        "cpu_seconds": cpu_seconds,
        "cpu_usage": cpu_seconds / wall_seconds * 100.0,
    }


def main() -> int:
    args = parse_arguments()

    import pygame

    pygame.init()

    try:
        width, height = (int(part) for part in args.size.lower().split("x"))
    except ValueError:
        print(f"Ukuran '{args.size}' tidak dikenali; pakai bentuk 720x480.")
        return 1

    try:
        caps = [int(part) for part in args.caps.split(",")]
    except ValueError:
        print(f"Daftar batas '{args.caps}' tidak dikenali; pakai bentuk 30,60,120,0.")
        return 1

    print("=" * 66)
    print(" PENGUKURAN PENGARUH BATAS LAJU BINGKAI")
    print(f" Lama setiap pengujian: {args.duration:.1f} detik")
    print(f" Pengandar video      : {pygame.display.get_driver()}")
    print("=" * 66)
    print()
    print(f"{'Batas':>7} {'Bingkai':>9} {'Laju':>11} "
          f"{'Waktu prosesor':>16} {'Pemakaian':>11}")
    print("-" * 66)

    for cap in caps:
        result = run_cycle(pygame, (width, height), cap, args.duration)
        label = "tanpa" if cap == 0 else str(cap)
        print(f"{label:>7} {result['frames']:>9.0f} "
              f"{result['rate']:>8.1f} FPS "
              f"{result['cpu_seconds']:>14.2f} s "
              f"{result['cpu_usage']:>9.1f} %")

    print("-" * 66)
    print()
    print("Catatan: pengukuran dilakukan tanpa jendela, sehingga angkanya")
    print("berbeda dari pengukuran pada jendela sungguhan. Yang dibandingkan")
    print("adalah hubungan antara batas laju dan pemakaian prosesor.")

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Gerak objek berbasis vektor dan selang waktu.

Sebuah persegi digerakkan dengan tombol WASD atau tombol panah. Kecepatan
dinyatakan dalam piksel per detik, lalu dikalikan selang waktu satu bingkai,
sehingga jarak yang ditempuh setiap detik selalu sama berapa pun laju
bingkainya.

Posisi disimpan sebagai Vector2 bertipe pecahan, sedangkan gambar ditempelkan
memakai Rect bertipe bilangan bulat. Penyelarasan keduanya diperlihatkan pada
jendela, agar perilakunya dapat Anda amati langsung.

Pengendalian:
    W atau panah atas  : bergerak ke atas
    A atau panah kiri  : bergerak ke kiri
    S atau panah bawah : bergerak ke bawah
    D atau panah kanan : bergerak ke kanan
    ESC                : mengakhiri program

Pemakaian:
    python ch05_gerak.py
    python ch05_gerak.py --speed 300
    python ch05_gerak.py --fps 30
    python ch05_gerak.py --frames 120                  (uji tanpa jendela)
    python ch05_gerak.py --frames 120 --auto-direction kanan
"""

from __future__ import annotations

import argparse
import sys

BACKGROUND_COLOR = (24, 32, 52)
PLAYER_COLOR = (46, 117, 182)
TEXT_COLOR = (255, 255, 255)
HINT_COLOR = (150, 165, 190)

DEFAULT_SPEED = 200.0        # piksel per detik
DEFAULT_FPS = 60
PLAYER_SIZE = 40             # sisi persegi, dalam piksel

# Arah tetap untuk pengujian tanpa papan tombol. Pada koordinat layar, sumbu
# tegak menuju ke bawah, sehingga arah "atas" bernilai negatif.
AUTO_DIRECTIONS = {
    "kanan": (1, 0),
    "kiri": (-1, 0),
    "atas": (0, -1),
    "bawah": (0, 1),
    "diagonal": (1, 1),
}


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Gerak objek berbasis vektor")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                        help="kecepatan gerak dalam piksel per detik")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-direction", choices=sorted(AUTO_DIRECTIONS),
                        default="",
                        help="arah tetap untuk pengujian tanpa papan tombol")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


def read_direction(pygame, auto_direction: str):
    """Tahap masukan. Menyusun vektor arah dari tombol yang sedang ditahan.

    Vektor yang dikembalikan belum dinormalkan; panjangnya bernilai satu
    apabila hanya satu tombol ditekan, dan bernilai akar dua apabila dua tombol
    ditekan bersamaan.
    """
    if auto_direction:
        dx, dy = AUTO_DIRECTIONS[auto_direction]
        return pygame.Vector2(dx, dy)

    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction.x -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction.x += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        direction.y -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direction.y += 1
    return direction


def update_position(pygame, position, direction, speed, delta_seconds,
                    screen_size):
    """Tahap pembaruan. Mengembalikan posisi baru dan kecepatan saat ini.

    Posisi diperbarui dengan perpindahan, yaitu kecepatan dikalikan selang
    waktu. Inilah yang membuat laju gerak tidak bergantung pada laju bingkai.
    """
    if direction.length_squared() > 0:
        # Vektor arah dinormalkan menjadi panjang satu, lalu dikalikan
        # kecepatan. Tanpa langkah ini, gerak diagonal menjadi akar dua kali
        # lebih cepat daripada gerak lurus.
        velocity = direction.normalize() * speed
    else:
        velocity = pygame.Vector2(0, 0)

    position = position + velocity * delta_seconds

    # Batasi agar persegi tetap berada di dalam jendela.
    width, height = screen_size
    half = PLAYER_SIZE / 2
    position.x = max(half, min(width - half, position.x))
    position.y = max(half, min(height - half, position.y))

    return position, velocity


def draw_window(pygame, screen, font, position, player_rect, velocity,
                measured_fps, average_speed, elapsed_seconds) -> None:
    """Tahap penayangan. Menggambar seluruh isi jendela dari awal."""
    width, height = screen.get_size()
    screen.fill(BACKGROUND_COLOR)

    # Persegi digambar memakai Rect bertipe bilangan bulat, sedangkan posisi
    # yang sebenarnya disimpan sebagai pecahan.
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    lines = [
        f"Laju bingkai      : {measured_fps:7.1f} FPS",
        f"Waktu berjalan    : {elapsed_seconds:7.1f} detik",
        f"Posisi (pecahan)  : ({position.x:7.2f}, {position.y:7.2f})",
        f"Rect (bulat)      : ({player_rect.centerx:4d}, {player_rect.centery:4d})",
        f"Kecepatan         : {velocity.length():7.1f} piksel/detik",
        f"Kecepatan rata-rata: {average_speed:7.1f} piksel/detik",
    ]
    y = 30
    for line in lines:
        screen.blit(font.render(line, True, TEXT_COLOR), (30, y))
        y += 26

    hint = font.render(
        "WASD atau tombol panah untuk bergerak   ESC untuk keluar",
        True, HINT_COLOR)
    screen.blit(hint, (30, height - 40))


def main() -> int:
    args = parse_arguments()

    import pygame

    pygame.init()
    screen = pygame.display.set_mode((760, 520))
    pygame.display.set_caption("Bab V - gerak berbasis selang waktu")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    screen_size = screen.get_size()
    position = pygame.Vector2(screen_size[0] / 2, screen_size[1] / 2)
    player_rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)

    frame_count = 0
    delta_seconds = 0.0
    moving_seconds = 0.0
    moved_distance = 0.0
    running = True
    start_ticks = pygame.time.get_ticks()

    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        # ---------- Tahap 1: membaca masukan ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        direction = read_direction(pygame, args.auto_direction)

        # ---------- Tahap 2: memperbarui keadaan ----------
        previous_position = position.copy()
        position, velocity = update_position(
            pygame, position, direction, args.speed, delta_seconds, screen_size)

        # Jarak tempuh diukur dari perubahan posisi yang sesungguhnya, bukan
        # dari kecepatan yang ditetapkan. Dengan begitu, kecepatan terukur
        # benar-benar hasil pengukuran dan bukan sekadar pengulangan angka
        # yang dimasukkan.
        step = position - previous_position
        if step.length_squared() > 0:
            moved_distance += step.length()
            moving_seconds += delta_seconds

        # Rect diselaraskan dengan posisi pecahan memakai pembulatan. Angka
        # dibulatkan, bukan dipotong, agar gerak tidak tampak tersendat.
        player_rect.center = (round(position.x), round(position.y))

        frame_count += 1
        measured_fps = clock.get_fps()
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
        if moving_seconds > 0:
            average_speed = moved_distance / moving_seconds
        else:
            average_speed = 0.0

        # ---------- Tahap 3: menayangkan ----------
        draw_window(pygame, screen, font, position, player_rect, velocity,
                    measured_fps, average_speed, elapsed_seconds)
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frame_count >= args.frames:
            running = False

    total_seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0
    pygame.quit()

    print(f"Bingkai dijalankan   : {frame_count}")
    print(f"Waktu berjalan       : {total_seconds:.2f} detik")
    print(f"Kecepatan ditetapkan : {args.speed:.1f} piksel/detik")
    print(f"Jarak tempuh         : {moved_distance:.1f} piksel")
    print(f"Lama bergerak        : {moving_seconds:.2f} detik")
    if moving_seconds > 0:
        print(f"Kecepatan terukur    : {moved_distance / moving_seconds:.1f} piksel/detik")
    return 0


if __name__ == "__main__":
    sys.exit(main())

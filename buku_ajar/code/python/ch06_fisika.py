"""Fisika sederhana: gravitasi, lompatan, dan pantulan.

Program ini memuat dua benda yang dihitung memakai fungsi pembaruan yang sama,
tetapi dengan satu nilai yang berbeda yaitu koefisien restitusi.

    Pemain  : digerakkan tombol, jatuh karena gravitasi, mendarat di lantai
              tanpa memantul, dan dapat melompat ketika menyentuh lantai.
    Bola    : bergerak sendiri, memantul di lantai dan di kedua dinding
              dengan kecepatan yang menyusut setiap pantulan.

Pengendalian:
    A atau panah kiri  : bergerak ke kiri
    D atau panah kanan : bergerak ke kanan
    spasi, W, panah atas : melompat, hanya ketika menyentuh lantai
    ESC                : mengakhiri program

Pemakaian:
    python ch06_fisika.py
    python ch06_fisika.py --gravity 2400 --jump-speed 800
    python ch06_fisika.py --frames 180 --auto-jump 90    (uji tanpa jendela)
"""

from __future__ import annotations

import argparse
import sys

BACKGROUND_COLOR = (24, 32, 52)
FLOOR_COLOR = (90, 110, 150)
PLAYER_COLOR = (46, 117, 182)
BALL_COLOR = (200, 140, 60)
TEXT_COLOR = (255, 255, 255)
HINT_COLOR = (150, 165, 190)

GRAVITY = 1800.0          # piksel per detik kuadrat
JUMP_SPEED = 700.0        # piksel per detik, arah ke atas
MOVE_SPEED = 260.0        # piksel per detik, arah mendatar
BALL_SPEED = 320.0        # piksel per detik, arah mendatar
PLAYER_SIZE = 36
BALL_SIZE = 26
PLAYER_RESTITUTION = 0.0  # pemain mendarat tanpa memantul
BALL_RESTITUTION = 0.8    # bola kehilangan 20 persen kecepatan setiap pantulan
MIN_BOUNCE_SPEED = 60.0   # di bawah nilai ini, pantulan dihentikan
DEFAULT_FPS = 60


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Fisika sederhana Pygame")
    parser.add_argument("--gravity", type=float, default=GRAVITY,
                        help="percepatan gravitasi, piksel per detik kuadrat")
    parser.add_argument("--jump-speed", type=float, default=JUMP_SPEED,
                        help="kecepatan awal lompatan, piksel per detik")
    parser.add_argument("--restitution", type=float, default=BALL_RESTITUTION,
                        help="koefisien restitusi bola, antara 0 dan 1")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-direction", choices=("kanan", "kiri"), default="",
                        help="arah mendatar tetap untuk pengujian")
    parser.add_argument("--auto-jump", type=int, default=0, metavar="N",
                        help="kirim peristiwa lompatan setiap N bingkai")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


def update_body(position, velocity, delta_seconds, half, floor_y, width,
                gravity, restitution):
    """Memperbarui satu benda: gravitasi, lantai, dan dinding.

    Mengembalikan posisi, kecepatan, serta keterangan apakah benda memantul di
    lantai atau di dinding pada bingkai ini.
    """
    # Tingkat pertama: percepatan mengubah kecepatan.
    velocity.y += gravity * delta_seconds

    # Tingkat kedua: kecepatan mengubah posisi, memakai kecepatan yang baru
    # saja diperbarui. Urutan ini sama dengan kaidah Euler semi-implisit.
    position = position + velocity * delta_seconds

    hit_floor = False
    hit_wall = False

    # Lantai.
    if position.y + half >= floor_y:
        position.y = floor_y - half
        if velocity.y > 0:
            velocity.y = -velocity.y * restitution
            if abs(velocity.y) < MIN_BOUNCE_SPEED:
                velocity.y = 0.0
            else:
                hit_floor = True

    # Dinding kiri dan kanan.
    if position.x - half < 0:
        position.x = half
        velocity.x = abs(velocity.x) * restitution
        hit_wall = True
    elif position.x + half > width:
        position.x = width - half
        velocity.x = -abs(velocity.x) * restitution
        hit_wall = True

    return position, velocity, hit_floor, hit_wall


def draw_window(pygame, screen, font, args, player_position, ball_position,
                player_rect, ball_rect, player_velocity, ball_velocity,
                measured_fps, on_ground, height_reached, jumps, bounces) -> None:
    """Tahap penayangan. Menggambar seluruh isi jendela dari awal."""
    width, height = screen.get_size()
    floor_y = height - 60

    screen.fill(BACKGROUND_COLOR)

    # Lantai sebagai garis mendatar.
    pygame.draw.line(screen, FLOOR_COLOR, (0, floor_y), (width, floor_y), 3)

    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, BALL_COLOR, ball_rect)

    lines = [
        f"Laju bingkai     : {measured_fps:7.1f} FPS",
        f"Pemain  posisi   : ({player_position.x:6.1f}, {player_position.y:6.1f})",
        f"        kecepatan: ({player_velocity.x:6.1f}, {player_velocity.y:6.1f})",
        f"        menyentuh lantai: {'ya' if on_ground else 'tidak'}",
        f"Bola    posisi   : ({ball_position.x:6.1f}, {ball_position.y:6.1f})",
        f"        kecepatan: ({ball_velocity.x:6.1f}, {ball_velocity.y:6.1f})",
        f"Lompatan         : {jumps:3d}    Pantulan bola: {bounces:3d}",
        f"Tinggi tertinggi : {height_reached:6.1f} piksel di atas lantai",
    ]
    y = 26
    for line in lines:
        screen.blit(font.render(line, True, TEXT_COLOR), (26, y))
        y += 24

    hint = font.render(
        "A/D atau panah: bergerak   spasi/W: melompat   ESC: keluar",
        True, HINT_COLOR)
    screen.blit(hint, (26, floor_y + 22))


def main() -> int:
    args = parse_arguments()

    import pygame

    pygame.init()
    screen = pygame.display.set_mode((780, 560))
    pygame.display.set_caption("Bab VI - gravitasi, lompatan, dan pantulan")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    width, height = screen.get_size()
    floor_y = height - 60

    # Keadaan pemain dan bola disimpan di luar perulangan agar bertahan dari
    # satu bingkai ke bingkai berikutnya.
    player_position = pygame.Vector2(width / 2, floor_y - PLAYER_SIZE / 2)
    player_velocity = pygame.Vector2(0, 0)
    ball_position = pygame.Vector2(120, floor_y - BALL_SIZE / 2 - 200)
    ball_velocity = pygame.Vector2(BALL_SPEED, 0)

    player_rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
    ball_rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

    frame_count = 0
    delta_seconds = 0.0
    on_ground = True
    jumps = 0
    bounces = 0
    height_reached = 0.0
    running = True

    if args.auto_close and not args.frames:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    while running:
        # ---------- Tahap 1: membaca masukan ----------
        direction_x = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    # Lompatan dibaca sebagai peristiwa, bukan sebagai keadaan
                    # tombol, agar menahan tombol tidak menghasilkan lompatan
                    # berulang-ulang.
                    if on_ground:
                        player_velocity.y = -args.jump_speed
                        on_ground = False
                        jumps += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction_x += 1
        if args.auto_direction == "kanan":
            direction_x = 1
        elif args.auto_direction == "kiri":
            direction_x = -1

        if args.auto_jump and frame_count % args.auto_jump == 0:
            pygame.event.post(pygame.event.Event(
                pygame.KEYDOWN, key=pygame.K_SPACE))

        # ---------- Tahap 2: memperbarui keadaan ----------
        player_velocity.x = direction_x * MOVE_SPEED

        player_position, player_velocity, hit_floor, hit_wall = update_body(
            player_position, player_velocity, delta_seconds, PLAYER_SIZE / 2,
            floor_y, width, args.gravity, PLAYER_RESTITUTION)

        ball_position, ball_velocity, ball_hit_floor, ball_hit_wall = update_body(
            ball_position, ball_velocity, delta_seconds, BALL_SIZE / 2,
            floor_y, width, args.gravity, args.restitution)

        if ball_hit_floor or ball_hit_wall:
            bounces += 1

        # Pemain dianggap menyentuh lantai apabila badannya bersandar pada
        # lantai dan kecepatan tegaknya tidak lagi mengarah ke bawah.
        on_ground = (player_position.y + PLAYER_SIZE / 2 >= floor_y - 0.5
                     and player_velocity.y >= 0)

        tinggi = floor_y - (player_position.y + PLAYER_SIZE / 2)
        if tinggi > height_reached:
            height_reached = tinggi

        player_rect.center = (round(player_position.x), round(player_position.y))
        ball_rect.center = (round(ball_position.x), round(ball_position.y))

        frame_count += 1
        measured_fps = clock.get_fps()

        # ---------- Tahap 3: menayangkan ----------
        draw_window(pygame, screen, font, args, player_position, ball_position,
                    player_rect, ball_rect, player_velocity, ball_velocity,
                    measured_fps, on_ground, height_reached, jumps, bounces)
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frame_count >= args.frames:
            running = False

    pygame.quit()

    # Tinggi lompatan yang seharusnya, menurut perhitungan pada bab ini.
    teoretis = args.jump_speed ** 2 / (2 * args.gravity)
    print(f"Bingkai dijalankan   : {frame_count}")
    print(f"Gravitasi            : {args.gravity:.0f} piksel/detik kuadrat")
    print(f"Kecepatan lompatan   : {args.jump_speed:.0f} piksel/detik")
    print(f"Koefisien restitusi  : {args.restitution:.2f}")
    print(f"Lompatan dilakukan   : {jumps}")
    print(f"Pantulan bola        : {bounces}")
    print(f"Tinggi tertinggi     : {height_reached:.1f} piksel")
    print(f"Tinggi menurut hitungan: {teoretis:.1f} piksel")
    return 0


if __name__ == "__main__":
    sys.exit(main())

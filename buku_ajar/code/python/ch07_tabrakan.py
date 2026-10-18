"""Tabrakan pada permainan: pemain mengumpulkan kepingan dan menghindari rintangan.

Program ini memakai kelas pygame.sprite.Sprite untuk setiap benda dan wadah
pygame.sprite.Group untuk mengelolanya. Tabrakan diselesaikan sumbu demi sumbu:
gerak mendatar diperiksa lebih dahulu, baru gerak tegak. Cara itu membuat pemain
dapat mendarat di atas bongkahan sekaligus terhalang oleh sisinya.

Pengendalian:
    A atau panah kiri    : bergerak ke kiri
    D atau panah kanan   : bergerak ke kanan
    spasi, W, panah atas : melompat
    ESC                  : mengakhiri program

Pemakaian:
    python ch07_tabrakan.py
    python ch07_tabrakan.py --frames 400 --auto-run     (uji tanpa jendela)
"""

from __future__ import annotations

import argparse
import sys

import pygame

BACKGROUND_COLOR = (24, 32, 52)
PLATFORM_COLOR = (70, 88, 126)
PLAYER_COLOR = (46, 117, 182)
ITEM_COLOR = (222, 178, 66)
HAZARD_COLOR = (190, 74, 66)
TEXT_COLOR = (255, 255, 255)
HINT_COLOR = (150, 165, 190)

GRAVITY = 1900.0
MOVE_SPEED = 260.0
JUMP_SPEED = 720.0
DEFAULT_FPS = 60

# Ukuran jendela. Lebarnya dipakai untuk menahan pemain agar tidak berjalan
# keluar dari layar.
WINDOW_WIDTH = 820
WINDOW_HEIGHT = 560

# Susunan bongkahan: (x, y, lebar, tinggi), pada jendela berukuran 820x560.
PLATFORM_LAYOUT = (
    (0, 520, 820, 40),        # lantai
    (140, 400, 180, 22),
    (420, 320, 200, 22),
    (640, 430, 160, 22),
)

# Tempat kepingan dan rintangan.
ITEM_LAYOUT = ((200, 370), (500, 290), (700, 400), (330, 480), (120, 190))
HAZARD_LAYOUT = ((390, 494), (770, 494), (560, 494))


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Tabrakan pada permainan Pygame")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-run", action="store_true",
                        help="jalankan masukan otomatis untuk pengujian")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


class Platform(pygame.sprite.Sprite):
    """Bongkahan tempat pemain dapat mendarat dan terhalang oleh sisinya."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))


class Item(pygame.sprite.Sprite):
    """Kepingan yang dikumpulkan pemain."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((18, 18))
        self.image.fill(ITEM_COLOR)
        self.rect = self.image.get_rect(center=(x, y))


class Hazard(pygame.sprite.Sprite):
    """Rintangan yang mengurangi nyawa pemain."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((26, 26))
        self.image.fill(HAZARD_COLOR)
        self.rect = self.image.get_rect(midbottom=(x, y))


class Player(pygame.sprite.Sprite):
    """Pemain yang bergerak, jatuh, dan melompat."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 42))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        # Posisi yang sebenarnya disimpan sebagai pecahan, sedangkan rect
        # dipakai untuk menggambar dan memeriksa tabrakan.
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def jump(self) -> None:
        """Melompat, hanya apabila sedang bersandar pada sesuatu."""
        if self.on_ground:
            self.velocity.y = -JUMP_SPEED
            self.on_ground = False

    def update(self, delta_seconds: float, direction_x: int,
               platforms: pygame.sprite.Group) -> None:
        """Memperbarui gerak, lalu menyelesaikan tabrakan sumbu demi sumbu."""
        # --- Sumbu mendatar ---
        self.velocity.x = direction_x * MOVE_SPEED
        self.position.x += self.velocity.x * delta_seconds

        # Tepi jendela sebagai batas, agar pemain tidak berjalan keluar layar.
        half_width = self.rect.width / 2
        self.position.x = max(half_width,
                              min(WINDOW_WIDTH - half_width, self.position.x))

        self.rect.centerx = round(self.position.x)

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:
                    # Menabrak dari kiri: badan ditempelkan pada sisi kirinya.
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.rect.right
                self.position.x = self.rect.centerx

        # --- Sumbu tegak ---
        self.velocity.y += GRAVITY * delta_seconds
        self.position.y += self.velocity.y * delta_seconds
        self.rect.centery = round(self.position.y)

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    # Jatuh ke atas bongkahan: kaki diletakkan di permukaannya.
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0.0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    # Membentur langit-langit bongkahan.
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0.0
                self.position.y = self.rect.centery

    def teleport(self, x: float, y: float) -> None:
        """Memindahkan pemain ke tempat lain, misalnya sesudah terkena rintangan."""
        self.position.update(x, y)
        self.velocity.update(0, 0)
        self.rect.center = (round(x), round(y))


def build_level() -> tuple:
    """Menyusun kelompok bongkahan, kepingan, dan rintangan."""
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()
    hazards = pygame.sprite.Group()

    for data in PLATFORM_LAYOUT:
        platforms.add(Platform(*data))
    for x, y in ITEM_LAYOUT:
        items.add(Item(x, y))
    for x, y in HAZARD_LAYOUT:
        hazards.add(Hazard(x, y))

    return platforms, items, hazards


def count_overlaps(player: Player, platforms: pygame.sprite.Group) -> int:
    """Menghitung bongkahan yang badannya bertumpang tindih dengan pemain.

    Nilainya seharusnya selalu nol. Nilai selain nol menandakan penyelesaian
    tabrakan per sumbu tidak bekerja dengan benar.
    """
    return sum(1 for platform in platforms
               if player.rect.colliderect(platform.rect))


def main() -> int:
    args = parse_arguments()

    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.set_mode((820, 560))
    pygame.display.set_caption("Bab VII - tabrakan dan pengumpulan kepingan")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    platforms, items, hazards = build_level()
    player = Player(80, 470)

    score = 0
    collected = 0
    lives = 3
    hazard_hits = 0
    overlap_frames = 0
    frames = 0
    delta_seconds = 0.0
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
                    player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction_x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction_x += 1

        if args.auto_run:
            # Masukan otomatis untuk pengujian: bergerak ke kanan sambil
            # melompat secara berkala.
            direction_x = 1
            if frames % 40 == 0:
                player.jump()

        # ---------- Tahap 2: memperbarui keadaan ----------
        player.update(delta_seconds, direction_x, platforms)

        # Tabrakan dengan kepingan. Argumen ketiga bernilai True sehingga
        # kepingan yang tersentuh langsung dikeluarkan dari kelompoknya.
        hit_items = pygame.sprite.spritecollide(player, items, True)
        if hit_items:
            collected += len(hit_items)
            score += 10 * len(hit_items)

        # Tabrakan dengan rintangan. Kepingan tidak dihilangkan, sehingga
        # pemain dapat tersentuh berulang kali.
        hit_hazards = pygame.sprite.spritecollide(player, hazards, False)
        if hit_hazards:
            hazard_hits += 1
            lives -= 1
            player.teleport(80, 470)
            if lives <= 0:
                running = False

        # Pemeriksaan: pemain tidak boleh berada di dalam bongkahan.
        if count_overlaps(player, platforms) > 0:
            overlap_frames += 1

        frames += 1
        measured_fps = clock.get_fps()

        # ---------- Tahap 3: menayangkan ----------
        screen.fill(BACKGROUND_COLOR)
        platforms.draw(screen)
        items.draw(screen)
        hazards.draw(screen)
        screen.blit(player.image, player.rect)

        info = [
            f"Skor              : {score:4d}",
            f"Kepingan terkumpul: {collected:2d} dari {len(ITEM_LAYOUT)}",
            f"Nyawa             : {lives}",
            f"Laju bingkai      : {measured_fps:6.1f} FPS",
            f"Bersandar         : {'ya' if player.on_ground else 'tidak'}",
        ]
        y = 20
        for line in info:
            screen.blit(font.render(line, True, TEXT_COLOR), (20, y))
            y += 23

        hint = font.render(
            "A/D atau panah: bergerak   spasi/W: melompat   ESC: keluar",
            True, HINT_COLOR)
        screen.blit(hint, (20, 536))
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frames >= args.frames:
            running = False

    pygame.quit()

    print(f"Bingkai dijalankan       : {frames}")
    print(f"Kepingan terkumpul       : {collected} dari {len(ITEM_LAYOUT)}")
    print(f"Skor                     : {score}")
    print(f"Tersentuh rintangan      : {hazard_hits}")
    print(f"Bingkai bertumpang tindih: {overlap_frames}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

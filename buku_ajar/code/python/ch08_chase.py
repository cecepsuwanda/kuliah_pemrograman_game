"""Perilaku mengejar: NPC bergerak sendiri menuju posisi pemain.

Pandangan permainan ini adalah pandangan atas, sehingga tidak ada gravitasi.
Pemain digerakkan tombol, sedangkan NPC bergerak atas keputusannya sendiri:
apabila pemain berada di dalam jari-jari persepsinya, NPC mengejar dengan
kecepatan tetap; apabila sudah cukup dekat, NPC berhenti agar tidak bergetar
di atas pemain.

Garis arah dari setiap NPC menuju pemain digambar agar keputusannya dapat
diamati, demikian pula lingkaran jari-jari persepsi dan lingkaran jarak henti.

Pengendalian:
    W A S D atau tombol panah : menggerakkan pemain
    ESC                       : mengakhiri program

Pemakaian:
    python ch08_chase.py
    python ch08_chase.py --npc 5 --radius 260 --speed 170
    python ch08_chase.py --frames 300 --auto-run        (uji tanpa jendela)
    python ch08_chase.py --frames 300 --auto-run --naive (cara yang salah)
"""

from __future__ import annotations

import argparse
import math
import sys

import pygame

BACKGROUND_COLOR = (24, 32, 52)
PLAYER_COLOR = (46, 117, 182)
NPC_COLOR = (190, 74, 66)
NPC_IDLE_COLOR = (120, 120, 130)
LINE_COLOR = (222, 178, 66)
RADIUS_COLOR = (80, 100, 140)
STOP_COLOR = (70, 120, 90)
TEXT_COLOR = (255, 255, 255)
HINT_COLOR = (150, 165, 190)

WINDOW_WIDTH = 860
WINDOW_HEIGHT = 580

PLAYER_SPEED = 240.0
PLAYER_SIZE = 30
NPC_SIZE = 26

DEFAULT_NPC = 3
DEFAULT_RADIUS = 240.0
DEFAULT_SPEED = 150.0
DEFAULT_STOP = 30.0
DEFAULT_FPS = 60


def parse_arguments() -> argparse.Namespace:
    """Membaca pilihan pada baris perintah."""
    parser = argparse.ArgumentParser(description="Perilaku mengejar pada NPC")
    parser.add_argument("--npc", type=int, default=DEFAULT_NPC,
                        help="banyaknya NPC")
    parser.add_argument("--radius", type=float, default=DEFAULT_RADIUS,
                        help="jari-jari persepsi, dalam piksel")
    parser.add_argument("--speed", type=float, default=DEFAULT_SPEED,
                        help="kecepatan NPC, dalam piksel per detik")
    parser.add_argument("--stop", type=float, default=DEFAULT_STOP,
                        help="jarak henti, dalam piksel")
    parser.add_argument("--naive", action="store_true",
                        help="pakai cara yang salah: kecepatan diambil dari vektor jarak")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help="batas laju bingkai per detik")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti setelah sekian bingkai (0 = tanpa batas)")
    parser.add_argument("--auto-run", action="store_true",
                        help="gerakkan pemain secara otomatis untuk pengujian")
    parser.add_argument("--auto-close", action="store_true",
                        help="kirim peristiwa QUIT sendiri untuk pengujian")
    return parser.parse_args()


class Player(pygame.sprite.Sprite):
    """Pemain yang digerakkan tombol."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

    def update(self, delta_seconds: float, direction) -> None:
        """Memperbarui gerak pemain berdasarkan arah dari tombol."""
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * PLAYER_SPEED
        else:
            self.velocity = pygame.Vector2(0, 0)

        self.position += self.velocity * delta_seconds
        half = PLAYER_SIZE / 2
        self.position.x = max(half, min(WINDOW_WIDTH - half, self.position.x))
        self.position.y = max(half, min(WINDOW_HEIGHT - half, self.position.y))
        self.rect.center = (round(self.position.x), round(self.position.y))


class Npc(pygame.sprite.Sprite):
    """NPC yang mengejar pemain apabila pemain berada di dalam jangkauannya."""

    def __init__(self, x: float, y: float, radius: float, speed: float,
                 stop_distance: float, naive: bool) -> None:
        super().__init__()
        self.image = pygame.Surface((NPC_SIZE, NPC_SIZE))
        self.image.fill(NPC_COLOR)
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.speed = speed
        self.stop_distance = stop_distance
        self.naive = naive
        self.chasing = False
        self.distance = 0.0

    def update(self, delta_seconds: float, player: Player) -> None:
        """Memperbarui gerak NPC menurut jarak dan arah terhadap pemain."""
        to_player = player.position - self.position
        self.distance = to_player.length()

        if self.distance <= self.stop_distance:
            # Sudah cukup dekat: berhenti, agar tidak bergetar di atas pemain.
            self.chasing = False
            self.velocity = pygame.Vector2(0, 0)
        elif self.distance <= self.radius:
            self.chasing = True
            if self.naive:
                # Cara yang salah: vektor jarak dipakai langsung sebagai
                # kecepatan, sehingga NPC bergerak makin cepat ketika jauh.
                self.velocity = to_player
            else:
                # Cara yang benar: arah dinormalkan lebih dahulu, lalu
                # dikalikan kecepatan, sehingga besarnya tetap berapa pun
                # jaraknya.
                self.velocity = to_player.normalize() * self.speed
        else:
            self.chasing = False
            self.velocity = pygame.Vector2(0, 0)

        self.position += self.velocity * delta_seconds
        half = NPC_SIZE / 2
        self.position.x = max(half, min(WINDOW_WIDTH - half, self.position.x))
        self.position.y = max(half, min(WINDOW_HEIGHT - half, self.position.y))
        self.rect.center = (round(self.position.x), round(self.position.y))

        if self.chasing:
            self.image.fill(NPC_COLOR)
        else:
            self.image.fill(NPC_IDLE_COLOR)


def auto_player_position(frames: int, fps: int) -> pygame.Vector2:
    """Mengembalikan posisi pemain pada jalur melingkar, untuk pengujian."""
    sudut = frames / fps * 0.9
    return pygame.Vector2(
        WINDOW_WIDTH / 2 + 250 * math.cos(sudut),
        WINDOW_HEIGHT / 2 + 170 * math.sin(sudut),
    )


def main() -> int:
    args = parse_arguments()

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Bab VIII - perilaku mengejar")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)

    player = Player(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    npcs = pygame.sprite.Group()
    for index in range(args.npc):
        sudut = index / max(1, args.npc) * 2 * math.pi
        x = WINDOW_WIDTH / 2 + 330 * math.cos(sudut)
        y = WINDOW_HEIGHT / 2 + 240 * math.sin(sudut)
        npcs.add(Npc(x, y, args.radius, args.speed, args.stop, args.naive))

    frames = 0
    delta_seconds = 0.0
    running = True

    # Untuk pengukuran: kecepatan NPC pertama pada jarak yang berbeda-beda.
    speed_samples: list[tuple[float, float]] = []

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
            player.position = auto_player_position(frames, args.fps)
            player.rect.center = (round(player.position.x),
                                  round(player.position.y))

        # ---------- Tahap 2: memperbarui keadaan ----------
        if not args.auto_run:
            player.update(delta_seconds, direction)

        chasing_count = 0
        for npc in npcs:
            npc.update(delta_seconds, player)
            if npc.chasing:
                chasing_count += 1

        first_npc = npcs.sprites()[0]
        if first_npc.chasing and frames % 10 == 0:
            speed_samples.append((first_npc.distance, first_npc.velocity.length()))

        frames += 1
        measured_fps = clock.get_fps()

        # ---------- Tahap 3: menayangkan ----------
        screen.fill(BACKGROUND_COLOR)

        for npc in npcs:
            # Lingkaran jari-jari persepsi dan jarak henti.
            pygame.draw.circle(screen, RADIUS_COLOR,
                               (round(npc.position.x), round(npc.position.y)),
                               int(npc.radius), 1)
            pygame.draw.circle(screen, STOP_COLOR,
                               (round(npc.position.x), round(npc.position.y)),
                               int(npc.stop_distance), 1)
            # Garis arah menuju pemain.
            pygame.draw.line(screen, LINE_COLOR, npc.rect.center,
                             player.rect.center, 1)

        npcs.draw(screen)
        screen.blit(player.image, player.rect)

        info = [
            f"Bingkai       : {frames:5d}",
            f"Laju bingkai  : {measured_fps:6.1f} FPS",
            f"NPC mengejar  : {chasing_count} dari {args.npc}",
            f"Jari-jari     : {args.radius:.0f} piksel",
            f"Kecepatan NPC : {args.speed:.0f} piksel/detik",
        ]
        y = 18
        for line in info:
            screen.blit(font.render(line, True, TEXT_COLOR), (18, y))
            y += 21

        hint = font.render("WASD atau panah: gerakkan pemain   ESC: keluar",
                            True, HINT_COLOR)
        screen.blit(hint, (18, WINDOW_HEIGHT - 30))
        pygame.display.flip()

        # ---------- Pengendali waktu ----------
        delta_seconds = clock.tick(args.fps) / 1000.0

        if args.frames and frames >= args.frames:
            running = False

    pygame.quit()

    print(f"Bingkai dijalankan    : {frames}")
    print(f"Cara gerak            : {'naif' if args.naive else 'dinormalkan'}")
    print(f"Kecepatan ditetapkan  : {args.speed:.1f} piksel/detik")
    if speed_samples:
        speeds = [kecepatan for _, kecepatan in speed_samples]
        print(f"Kecepatan terukur     : {min(speeds):.1f} sampai {max(speeds):.1f} piksel/detik")
        print(f"Jarak saat diukur     : {min(j for j, _ in speed_samples):.1f} "
              f"sampai {max(j for j, _ in speed_samples):.1f} piksel")
    return 0


if __name__ == "__main__":
    sys.exit(main())

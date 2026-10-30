"""Jendela dan siklus permainan Gudang Artefak.

Sesi ini menambahkan pemain yang bergerak mendatar. Posisinya diperbarui
memakai kecepatan dikali selang waktu, sehingga gerak tidak bergantung pada
laju bingkai.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Player


class Game:
    """Memegang jendela, pemain, dan siklus permainan."""

    def __init__(self, args) -> None:
        self.args = args
        pygame.init()
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        self.frames = 0
        self.running = True

        # Pemain mulai di tengah jendela.
        self.player = Player(S.WINDOW_WIDTH / 2 - S.PLAYER_SIZE / 2,
                             S.WINDOW_HEIGHT / 2 - S.PLAYER_SIZE / 2)
        self.player.bounds = (args.width, args.height)

    def run(self) -> int:
        """Menjalankan siklus sampai jendela ditutup atau batas bingkai tiba."""
        while self.running:
            # Pengendali waktu: tick() membatasi laju bingkai sekaligus
            # mengembalikan selang waktu satu bingkai dalam milidetik.
            delta_seconds = self.clock.tick(self.args.fps) / 1000.0

            self.handle_events()
            self.update(delta_seconds)
            self.draw()
            pygame.display.flip()

            self.frames += 1
            if self.frames % 30 == 0:
                pygame.display.set_caption(
                    f"{S.TITLE} | {int(self.clock.get_fps())} FPS")

            if self.args.frames and self.frames >= self.args.frames:
                self.running = False
            if self.args.auto_close and self.frames >= 2:
                break

        pygame.quit()
        return 0

    def handle_events(self) -> None:
        """Menutup jendela atau menekan ESC mengakhiri program."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self, delta_seconds: float) -> None:
        """Membaca tombol arah lalu memperbarui posisi pemain."""
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player.update(delta_seconds, direction)

    def draw(self) -> None:
        """Menggambar latar dan pemain."""
        self.screen.fill(S.BACKGROUND)
        self.screen.blit(self.player.image, self.player.rect)

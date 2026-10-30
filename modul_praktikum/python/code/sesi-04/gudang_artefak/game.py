"""Jendela dan siklus permainan Gudang Artefak.

Sesi ini menambahkan gravitasi, lompatan, dan pantulan. Pemain bergerak di
antara lantai dan rak yang masih berupa daftar pygame.Rect.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Player
from .levels import SPAWN, build_rak


class Game:
    """Memegang jendela, pemain, dan perabot level Rak."""

    def __init__(self, args) -> None:
        self.args = args
        pygame.init()
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        self.frames = 0
        self.running = True

        self.player = Player(*SPAWN)
        self.solids = build_rak()

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
        """Menutup jendela, keluar dengan ESC, atau melompat dengan spasi."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self, delta_seconds: float) -> None:
        """Membaca tombol arah lalu memperbarui fisika pemain."""
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player.update_side(delta_seconds, direction, self.solids)

    def draw(self) -> None:
        """Menggambar latar, lantai, rak, dan pemain."""
        self.screen.fill(S.BACKGROUND)
        for rect in self.solids:
            color = S.FLOOR_COLOR if rect.y >= 540 else S.RACK_COLOR
            pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(self.player.image, self.player.rect)

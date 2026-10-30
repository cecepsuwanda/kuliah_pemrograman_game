"""Jendela dan siklus permainan Gudang Artefak.

Sesi ini menambahkan artefak, peti, dan pintu. Pemain mengumpulkan artefak
untuk membuka pintu, menghindari peti yang mengurangi nyawa, lalu menyentuh
pintu yang sudah terbuka untuk menyelesaikan level.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Player
from .levels import ARTEFACT_LAYOUT, build_rak


class Game:
    """Memegang jendela, pemain, dan seluruh isi level Rak."""

    def __init__(self, args) -> None:
        self.args = args
        pygame.init()
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.small = pygame.font.Font(None, 22)
        self.frames = 0
        self.running = True
        self.reset()

    # --- penyiapan ----------------------------------------------------
    def reset(self) -> None:
        """Mengembalikan skor, nyawa, dan isi level ke keadaan awal."""
        self.score = 0
        self.lives = S.START_LIVES
        self.mode = "rak"
        self.message = ""
        self.artefacts_left = len(ARTEFACT_LAYOUT)
        self._load_rak()

    def _load_rak(self) -> None:
        self.rak = build_rak()
        self.player = Player(*self.rak["spawn"])
        self.solids = self.rak["solids"]
        self.rak["door"].set_open(False)

    # --- siklus -------------------------------------------------------
    def run(self) -> int:
        """Menjalankan siklus sampai jendela ditutup atau batas bingkai tiba."""
        while self.running:
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
        """Menutup jendela, melompat, atau mengulang setelah permainan usai."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.mode == "rak":
                    self.player.jump()
                elif event.key == pygame.K_r and self.mode in ("kalah",
                                                               "menang"):
                    self.reset()

    def update(self, delta_seconds: float) -> None:
        if self.mode == "rak":
            self._update_rak(delta_seconds)
        self.player.respawn_timer = max(0.0, self.player.respawn_timer
                                       - delta_seconds)

    # --- level Rak ----------------------------------------------------
    def _update_rak(self, delta_seconds: float) -> None:
        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) \
            - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        self.player.update_side(delta_seconds, direction, self.solids)

        # Artefak yang tersentuh langsung dikeluarkan dari kelompoknya.
        door = self.rak["door"]
        collected = pygame.sprite.spritecollide(self.player,
                                                self.rak["artefacts"], True)
        for _ in collected:
            self.score += S.ARTEFACT_POINTS
            self.artefacts_left -= 1
        door.set_open(self.artefacts_left == 0)

        # Peti tidak dihilangkan, tetapi pemain diberi waktu kebal sesaat
        # setelah kehilangan nyawa agar tidak tersentuh berulang kali.
        if self.player.respawn_timer <= 0.0:
            hit = pygame.sprite.spritecollide(self.player, self.rak["crates"],
                                              False)
            if hit:
                self._lose_life(self.rak["spawn"])

        if door.open and self.player.rect.colliderect(door.rect):
            self.mode = "menang"
            self.message = "Level Rak selesai."

    def _lose_life(self, spawn) -> None:
        self.lives -= 1
        if self.lives <= 0:
            self.mode = "kalah"
            self.message = "Nyawa habis. Tekan R untuk mencoba lagi."
            return
        self.player.respawn(spawn[0], spawn[1])

    # --- gambar -------------------------------------------------------
    def draw(self) -> None:
        self.screen.fill(S.BACKGROUND)
        if self.mode == "rak":
            self._draw_rak()
        else:
            self._draw_end()
        self._draw_hud()

    def _draw_rak(self) -> None:
        self.solids.draw(self.screen)
        self.rak["artefacts"].draw(self.screen)
        self.rak["crates"].draw(self.screen)
        self.screen.blit(self.rak["door"].image, self.rak["door"].rect)
        self.screen.blit(self.player.image, self.player.rect)

    def _draw_end(self) -> None:
        self.screen.blit(self.player.image, self.player.rect)
        text = self.font.render(self.message, True, S.TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(S.WINDOW_WIDTH // 2,
                                                     300)))

    def _draw_hud(self) -> None:
        judul = self.rak["name"]
        self.screen.blit(self.font.render(judul, True, S.TEXT_COLOR), (24, 18))
        info = f"Skor {self.score}   Nyawa {self.lives}"
        self.screen.blit(self.small.render(info, True, S.ARTEFACT_COLOR),
                         (24, 46))

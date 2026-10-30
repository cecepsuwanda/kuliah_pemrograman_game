"""Benda-benda yang hidup di dalam permainan.

Sesi ini baru memuat pemain. Posisi disimpan sebagai Vector2 bertipe pecahan,
sedangkan rect bertipe bilangan bulat dipakai untuk menggambar.
"""

from __future__ import annotations

import pygame

from . import settings as S


class Player(pygame.sprite.Sprite):
    """Pemain yang bergerak mendatar mengikuti tombol."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((S.PLAYER_SIZE, S.PLAYER_SIZE))
        self.image.fill(S.PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        # Batas jendela tempat pemain dijepit. Game menyesuaikannya dengan
        # ukuran jendela yang benar-benar dipakai.
        self.bounds = (S.WINDOW_WIDTH, S.WINDOW_HEIGHT)

    def update(self, delta_seconds: float, direction: int) -> None:
        """Memperbarui posisi memakai kecepatan dikali selang waktu.

        Selang waktu membuat jarak tempuh per detik tetap sama walaupun laju
        bingkai berubah. Rect diselaraskan dengan pembulatan, bukan pemotongan,
        agar gerak tidak tampak tersendat.
        """
        self.position.x += direction * S.PLAYER_SPEED * delta_seconds

        # Pemain dijepit agar tidak berjalan keluar dari jendela.
        limit = self.bounds[0] - S.PLAYER_SIZE
        self.position.x = max(0.0, min(limit, self.position.x))
        self.rect.x = round(self.position.x)

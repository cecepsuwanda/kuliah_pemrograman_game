"""Benda-benda yang hidup di dalam permainan.

Pemain pada sesi ini jatuh karena gravitasi, mendarat di lantai atau rak, dan
dapat melompat. Tabrakan diselesaikan sumbu demi sumbu: gerak mendatar
diperiksa lebih dahulu, baru gerak tegak.
"""

from __future__ import annotations

import pygame

from . import settings as S


class Player(pygame.sprite.Sprite):
    """Pemain pada level samping."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = pygame.Surface((S.PLAYER_SIZE, S.PLAYER_SIZE))
        self.image.fill(S.PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False

    def update_side(self, delta_seconds: float, direction: int,
                    solids: list[pygame.Rect]) -> None:
        """Gerak mendatar, gravitasi, dan penyelesaian tabrakan per sumbu.

        Gravitasi mengubah kecepatan tegak lebih dahulu, lalu kecepatan yang
        baru itu mengubah posisi. Urutan ini sama dengan kaidah Euler
        semi-implisit yang dipakai pada Bab VI.
        """
        self.velocity.x = direction * S.PLAYER_SPEED
        self.velocity.y += S.GRAVITY * delta_seconds
        self.on_ground = False

        # --- Sumbu mendatar ---
        self.position.x += self.velocity.x * delta_seconds
        self.rect.x = round(self.position.x)
        self._resolve_horizontal(solids)

        # --- Sumbu tegak ---
        self.position.y += self.velocity.y * delta_seconds
        self.rect.y = round(self.position.y)
        self._resolve_vertical(solids)

    def _resolve_horizontal(self, solids: list[pygame.Rect]) -> None:
        for solid in solids:
            if not self.rect.colliderect(solid):
                continue
            if self.velocity.x > 0:
                self.rect.right = solid.left
            elif self.velocity.x < 0:
                self.rect.left = solid.right
            # Dinding memantulkan pemain selama kecepatannya masih cukup
            # besar; di bawah ambang itu pemain berhenti agar tidak bergetar.
            if abs(self.velocity.x) >= S.MIN_BOUNCE_SPEED:
                self.velocity.x = -self.velocity.x * S.WALL_RESTITUTION
            else:
                self.velocity.x = 0.0
            self.position.x = self.rect.x

    def _resolve_vertical(self, solids: list[pygame.Rect]) -> None:
        for solid in solids:
            if not self.rect.colliderect(solid):
                continue
            if self.velocity.y > 0:
                self.rect.bottom = solid.top
                self.velocity.y = 0.0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = solid.bottom
                self.velocity.y = 0.0
            self.position.y = self.rect.y

    def jump(self) -> None:
        """Melompat hanya bila pemain sedang menyentuh lantai atau rak."""
        if self.on_ground:
            self.velocity.y = -S.JUMP_SPEED
            self.on_ground = False

"""Benda-benda yang hidup di dalam permainan.

Setiap benda adalah pygame.sprite.Sprite sehingga dapat dimasukkan ke Group
dan diperiksa tabrakannya dengan spritecollide atau groupcollide. Semua
gambar dibuat dari bentuk pygame; tidak ada berkas aset yang dimuat.
"""

from __future__ import annotations

import pygame

from . import settings as S


def _square(size: int, fill, border=None, radius: int = 3) -> pygame.Surface:
    """Membuat permukaan persegi berwarna tanpa memuat berkas gambar."""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surface, fill, surface.get_rect(), border_radius=radius)
    if border is not None:
        pygame.draw.rect(surface, border, surface.get_rect(), 2,
                         border_radius=radius)
    return surface


class Player(pygame.sprite.Sprite):
    """Pemain pada level samping."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.image = _square(S.PLAYER_SIZE, S.PLAYER_COLOR,
                             (200, 220, 240))
        self.rect = self.image.get_rect(topleft=(round(x), round(y)))
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.respawn_timer = 0.0

    def update_side(self, delta_seconds: float, direction: int,
                    solids: pygame.sprite.Group) -> None:
        """Gerak mendatar, gravitasi, dan penyelesaian tabrakan per sumbu."""
        self.velocity.x = direction * S.PLAYER_SPEED
        self.velocity.y += S.GRAVITY * delta_seconds
        self.on_ground = False

        self.position.x += self.velocity.x * delta_seconds
        self.rect.x = round(self.position.x)
        self._resolve_horizontal(solids)

        self.position.y += self.velocity.y * delta_seconds
        self.rect.y = round(self.position.y)
        self._resolve_vertical(solids)

    def _resolve_horizontal(self, solids) -> None:
        for solid in solids:
            if not self.rect.colliderect(solid.rect):
                continue
            if self.velocity.x > 0:
                self.rect.right = solid.rect.left
            elif self.velocity.x < 0:
                self.rect.left = solid.rect.right
            # Dinding memantulkan pemain selama kecepatannya masih cukup
            # besar; di bawah ambang itu pemain berhenti agar tidak bergetar.
            if abs(self.velocity.x) >= S.MIN_BOUNCE_SPEED:
                self.velocity.x = -self.velocity.x * S.WALL_RESTITUTION
            else:
                self.velocity.x = 0.0
            self.position.x = self.rect.x

    def _resolve_vertical(self, solids) -> None:
        for solid in solids:
            if not self.rect.colliderect(solid.rect):
                continue
            if self.velocity.y > 0:
                self.rect.bottom = solid.rect.top
                self.velocity.y = 0.0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = solid.rect.bottom
                self.velocity.y = 0.0
            self.position.y = self.rect.y

    def jump(self) -> None:
        """Melompat hanya bila pemain sedang menyentuh lantai atau rak."""
        if self.on_ground:
            self.velocity.y = -S.JUMP_SPEED
            self.on_ground = False

    def respawn(self, x: float, y: float) -> None:
        """Mengembalikan pemain ke titik awal dan memberi waktu kebal."""
        self.position.update(x, y)
        self.rect.topleft = (round(x), round(y))
        self.velocity.update(0, 0)
        self.respawn_timer = S.RESPAWN_SECONDS


class Solid(pygame.sprite.Sprite):
    """Lantai atau rak pada level samping."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 color=S.RACK_COLOR) -> None:
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Artefact(pygame.sprite.Sprite):
    """Artefak yang menambah skor ketika disentuh."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        size = 22
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, S.ARTEFACT_COLOR,
                            [(size // 2, 0), (size, size // 2),
                             (size // 2, size), (0, size // 2)])
        self.rect = self.image.get_rect(center=(x, y))


class Crate(pygame.sprite.Sprite):
    """Peti yang mengurangi nyawa ketika disentuh."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = _square(34, S.CRATE_COLOR, (140, 50, 44))
        pygame.draw.line(self.image, (140, 50, 44), (4, 4), (30, 30), 2)
        pygame.draw.line(self.image, (140, 50, 44), (30, 4), (4, 30), 2)
        self.rect = self.image.get_rect(center=(x, y))


class Door(pygame.sprite.Sprite):
    """Pintu keluar. Terbuka setelah semua artefak terkumpul."""

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((46, 78), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.open = False
        self._paint()

    def _paint(self) -> None:
        self.image.fill((0, 0, 0, 0))
        color = S.DOOR_COLOR if self.open else (90, 100, 120)
        pygame.draw.rect(self.image, color, self.image.get_rect(),
                         border_radius=4)
        pygame.draw.rect(self.image, (20, 26, 40), self.image.get_rect(), 3,
                         border_radius=4)
        if self.open:
            pygame.draw.circle(self.image, (235, 240, 250), (36, 40), 3)

    def set_open(self, value: bool) -> None:
        if self.open != value:
            self.open = value
            self._paint()

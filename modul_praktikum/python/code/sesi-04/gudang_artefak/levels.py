"""Data level Rak.

Level Rak bertampilan samping dan memakai lantai serta rak. Pada sesi ini
perabot masih berupa pygame.Rect biasa; kelas Sprite menyusul pada sesi
berikutnya.
"""

from __future__ import annotations

import pygame

# Susunan lantai dan rak: (x, y, lebar, tinggi) pada jendela 960 x 600.
PLATFORM_LAYOUT = (
    (0, 552, 960, 48),        # lantai
    (150, 438, 170, 18),
    (400, 352, 170, 18),
    (660, 438, 160, 18),
    (300, 258, 150, 18),
    (620, 232, 200, 18),
)

# Tempat pemain mulai, sebagai pojok kiri atas badannya.
SPAWN = (70, 500)


def build_rak() -> list[pygame.Rect]:
    """Mengembalikan daftar Rect lantai dan rak."""
    return [pygame.Rect(x, y, width, height)
            for x, y, width, height in PLATFORM_LAYOUT]

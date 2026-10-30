"""Data level Rak.

Level Rak bertampilan samping dan memakai lantai serta rak. Susunan perabot,
artefak, peti, dan pintu sama dengan susunan yang dipakai pada sesi 09.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Artefact, Crate, Door, Solid

# Susunan lantai dan rak: (x, y, lebar, tinggi).
PLATFORM_LAYOUT = (
    (0, 552, 960, 48),        # lantai
    (150, 438, 170, 18),
    (400, 352, 170, 18),
    (660, 438, 160, 18),
    (300, 258, 150, 18),
    (620, 232, 200, 18),
)

# Titik pusat artefak dan peti, serta pojok kiri atas pintu.
ARTEFACT_LAYOUT = ((235, 408), (485, 322), (740, 408), (375, 228),
                   (720, 202), (110, 470))
CRATE_LAYOUT = ((430, 520), (560, 520), (830, 520))
DOOR_POSITION = (888, 456)
SPAWN = (70, 500)


def build_rak() -> dict:
    """Menyusun seluruh isi level Rak menjadi satu kamus."""
    solids = pygame.sprite.Group()
    for x, y, width, height in PLATFORM_LAYOUT:
        solids.add(Solid(x, y, width, height,
                         S.FLOOR_COLOR if y >= 540 else S.RACK_COLOR))

    artefacts = pygame.sprite.Group()
    for x, y in ARTEFACT_LAYOUT:
        artefacts.add(Artefact(x, y))

    crates = pygame.sprite.Group()
    for x, y in CRATE_LAYOUT:
        crates.add(Crate(x, y))

    door = Door(*DOOR_POSITION)
    return {"solids": solids, "artefacts": artefacts, "crates": crates,
            "door": door, "spawn": SPAWN, "name": "Level 1 - Rak"}

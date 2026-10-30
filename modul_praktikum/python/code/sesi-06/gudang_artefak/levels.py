"""Data kedua level Gudang Artefak.

Level Rak bertampilan samping dan memakai lantai serta rak. Level Lorong
bertampilan atas dan memakai grid. Pada sesi ini Lorong masih memakai satu
peta, yaitu skenario 1.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Artefact, Crate, Door, Solid

# --- Level 1: Rak -----------------------------------------------------
PLATFORM_LAYOUT = (
    (0, 552, 960, 48),        # lantai
    (150, 438, 170, 18),
    (400, 352, 170, 18),
    (660, 438, 160, 18),
    (300, 258, 150, 18),
    (620, 232, 200, 18),
)
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


# --- Level 2: Lorong --------------------------------------------------
# '#' dinding, '.' lantai, 'S' titik awal, 'E' pintu keluar.
SCENARIOS = {
    1: (
        "########################",
        "#S.....................#",
        "#......................#",
        "#......................#",
        "#....##..........##....#",
        "#......................#",
        "#......................#",
        "#......................#",
        "#......................#",
        "#....##..........##....#",
        "#......................#",
        "#....................E.#",
        "#......................#",
        "########################",
    ),
}

GUARD_START = {1: (12, 3)}


def build_lorong(scenario: int = 1) -> dict:
    """Menyusun peta Lorong beserta titik awal, pintu keluar, dan penjaga."""
    rows = SCENARIOS[scenario]
    walls = set()
    start = None
    exit_cell = None
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "#":
                walls.add((x, y))
            elif char == "S":
                start = (x, y)
            elif char == "E":
                exit_cell = (x, y)

    rects = [pygame.Rect(S.GRID_OFFSET_X + x * S.CELL,
                         S.GRID_OFFSET_Y + y * S.CELL, S.CELL, S.CELL)
             for x, y in walls]
    return {
        "rows": rows,
        "walls": walls,
        "wall_rects": rects,
        "start": start,
        "exit": exit_cell,
        "guard_start": GUARD_START[scenario],
        "name": "Level 2 - Lorong",
    }

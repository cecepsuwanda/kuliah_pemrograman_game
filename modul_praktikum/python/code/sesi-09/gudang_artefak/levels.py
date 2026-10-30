"""Data kedua level Gudang Artefak.

Level Rak bertampilan samping dan memakai lantai serta rak. Level Lorong
bertampilan atas dan memakai grid. Ketiga peta Lorong dipakai sebagai
tiga skenario uji pada sesi 09.
"""

from __future__ import annotations

import pygame

from . import settings as S
from .entities import Artefact, Crate, Door, Solid

# --- Level 1: Rak -----------------------------------------------------
PLATFORM_LAYOUT = (
    (0, 552, 960, 48),
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
RACK_GOAL = 6


def build_rak() -> dict:
    solids = pygame.sprite.Group()
    for x, y, w, h in PLATFORM_LAYOUT:
        solids.add(Solid(x, y, w, h,
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
    2: (
        "########################",
        "#S.....................#",
        "#.##################.#.#",
        "#..................#.#.#",
        "#.################.#.#.#",
        "#.#..............#.#.#.#",
        "#.#.############.#.#.#.#",
        "#.#.#..........#.#.#.#.#",
        "#.#.#.########.#.#.#.#.#",
        "#.#.#.#......#.#.#.#.#.#",
        "#.#.#.#.####.#.#.#.#.#.#",
        "#.#...#.#..#.#.#.#...#E#",
        "#.....#.#..#.#.#.#.....#",
        "########################",
    ),
    3: (
        "########################",
        "#S....................E#",
        "#......................#",
        "#.........#####........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#.........#...#........#",
        "#......................#",
        "#......................#",
        "########################",
    ),
}

PATROL_POINTS = {
    1: ((4, 2), (10, 2), (10, 12), (4, 12)),
    2: ((2, 1), (21, 1)),
    3: ((2, 2), (8, 2), (8, 11), (2, 11)),
}
GUARD_START = {1: (12, 3), 2: (12, 1), 3: (12, 2)}


def build_lorong(scenario: int) -> dict:
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
        "waypoints": PATROL_POINTS[scenario],
        "name": f"Level 2 - Lorong (skenario {scenario})",
    }

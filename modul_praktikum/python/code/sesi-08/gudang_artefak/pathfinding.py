"""Pencarian jalur A* pada grid.

Grid disimpan sebagai daftar baris teks. Karakter '#' adalah dinding dan
karakter lain adalah petak yang dapat dilalui. Biaya setiap langkah sama
(satu petak), sehingga f = g + h dengan h berupa jarak Manhattan.
"""

from __future__ import annotations

import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def build_grid(rows: tuple[str, ...]) -> tuple[set, int, int]:
    """Mengubah baris teks menjadi himpunan dinding dan ukuran grid."""
    walls = set()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char == "#":
                walls.add((x, y))
    height = len(rows)
    width = len(rows[0]) if rows else 0
    return walls, width, height


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Jarak Manhattan: selisih mendatar ditambah selisih tegak."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbours(cell: tuple[int, int], walls: set, width: int,
               height: int):
    """Empat petak tetangga yang berada di dalam peta dan bukan dinding."""
    x, y = cell
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
            yield (nx, ny)


def find_path(rows: tuple[str, ...], start: tuple[int, int],
              goal: tuple[int, int]):
    """Mengembalikan daftar petak dari start ke goal, atau daftar kosong.

    Biaya g dihitung dari jumlah langkah yang sudah ditempuh. Heuristik h
    memakai jarak Manhattan, yang tidak pernah melebih-lebihkan biaya
    sebenarnya pada grid empat arah.
    """
    walls, width, height = build_grid(rows)
    if start in walls or goal in walls:
        return []

    open_heap = [(manhattan(start, goal), 0, start)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    best_g = {start: 0}
    closed = set()

    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        if current == goal:
            return _reconstruct(came_from, current)
        closed.add(current)
        for nxt in neighbours(current, walls, width, height):
            new_g = g + 1
            if new_g < best_g.get(nxt, 10 ** 9):
                best_g[nxt] = new_g
                came_from[nxt] = current
                f = new_g + manhattan(nxt, goal)
                heapq.heappush(open_heap, (f, new_g, nxt))
    return []


def _reconstruct(came_from: dict, current: tuple[int, int]):
    """Menelusuri kembali dari tujuan ke titik awal."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

"""Mesin keadaan penjaga.

Bagian ini hanya memutuskan niat: berdiam, berpatroli, atau mengejar.
Perhitungan rute saat mengejar dikerjakan pathfinding.py; saat berpatroli
penjaga tetap menuju waypoint secara langsung.
"""

from __future__ import annotations

import pygame

from . import settings as S

IDLE = "idle"
PATROL = "patrol"
CHASE = "chase"


class GuardBrain:
    """Memilih keadaan penjaga berdasarkan jarak, waktu, dan cooldown."""

    def __init__(self, waypoints: tuple[tuple[int, int], ...]) -> None:
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.state = IDLE
        self.idle_timer = S.GUARD_IDLE_SECONDS
        self.lost_timer = 0.0
        self.radius = S.GUARD_RADIUS_CELLS * S.CELL

    def update(self, delta_seconds: float, guard_pos: pygame.Vector2,
               player_pos: pygame.Vector2) -> str:
        """Mengembalikan keadaan yang berlaku pada bingkai ini."""
        jarak = (player_pos - guard_pos).length()
        if self.state != CHASE and jarak <= self.radius:
            self.state = CHASE
            self.lost_timer = 0.0
        elif self.state == CHASE:
            if jarak <= self.radius:
                self.lost_timer = 0.0
            else:
                self.lost_timer += delta_seconds
                if self.lost_timer >= S.GUARD_GIVE_UP_SECONDS:
                    self.state = PATROL
        elif self.state == IDLE:
            self.idle_timer -= delta_seconds
            if self.idle_timer <= 0.0:
                self.state = PATROL
        return self.state

    def patrol_point(self) -> pygame.Vector2:
        """Titik patroli yang sedang dituju, dalam piksel."""
        cell = self.waypoints[self.waypoint_index]
        return pygame.Vector2(S.GRID_OFFSET_X + cell[0] * S.CELL + S.CELL / 2,
                               S.GRID_OFFSET_Y + cell[1] * S.CELL + S.CELL / 2)

    def next_patrol_point(self) -> None:
        """Berpindah ke titik patroli berikutnya secara berurutan."""
        self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)

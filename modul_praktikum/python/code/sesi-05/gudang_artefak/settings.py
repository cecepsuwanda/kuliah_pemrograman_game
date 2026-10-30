"""Pengaturan tetap untuk permainan Gudang Artefak.

Semua angka yang dipakai bersama dikumpulkan di sini agar mudah diubah dan
mudah dicari ketika terjadi masalah. Nilai fisika mengikuti contoh pada
Bab VI buku ajar.
"""

from __future__ import annotations

# --- Jendela -----------------------------------------------------------
TITLE = "Gudang Artefak"
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 600
FPS = 60

# --- Warna ------------------------------------------------------------
BACKGROUND = (24, 32, 52)
FLOOR_COLOR = (70, 88, 126)
RACK_COLOR = (96, 116, 158)
PLAYER_COLOR = (46, 117, 182)
ARTEFACT_COLOR = (222, 178, 66)
CRATE_COLOR = (190, 74, 66)
DOOR_COLOR = (60, 160, 110)
TEXT_COLOR = (235, 240, 250)

# --- Pemain dan fisika -------------------------------------------------
PLAYER_SIZE = 36
PLAYER_SPEED = 260.0        # piksel per detik
GRAVITY = 1900.0           # piksel per detik kuadrat
JUMP_SPEED = 720.0         # piksel per detik, arah ke atas
WALL_RESTITUTION = 0.8     # kecepatan setelah memantul = 0,8 kali semula
MIN_BOUNCE_SPEED = 60.0    # di bawah ini, pantulan dihentikan
RESPAWN_SECONDS = 1.0      # kebal sesaat setelah kehilangan nyawa

# --- Nyawa dan skor ---------------------------------------------------
START_LIVES = 3
ARTEFACT_POINTS = 10

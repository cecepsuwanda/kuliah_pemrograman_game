"""Pengaturan tetap untuk permainan Gudang Artefak.

Semua angka yang dipakai bersama dikumpulkan di sini agar mudah diubah dan
mudah dicari ketika terjadi masalah. Kecepatan pemain mengikuti contoh pada
Bab V buku ajar.
"""

from __future__ import annotations

# --- Jendela -----------------------------------------------------------
TITLE = "Gudang Artefak"
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 600
FPS = 60

# --- Warna ------------------------------------------------------------
BACKGROUND = (24, 32, 52)
PLAYER_COLOR = (46, 117, 182)

# --- Pemain -----------------------------------------------------------
PLAYER_SIZE = 36
PLAYER_SPEED = 260.0        # piksel per detik

"""Jendela dan siklus permainan Gudang Artefak.

Sesi ini mulai memakai siklus permainan yang sesungguhnya: masukan dibaca,
keadaan diperbarui, gambar disusun ulang, lalu ditayangkan berulang kali.
Keadaan yang diperbarui belum berisi apa pun; yang penting adalah pengendali
waktu dan laju bingkai.
"""

from __future__ import annotations

import pygame

from . import settings as S


class Game:
    """Memegang jendela dan menjalankan siklus permainan."""

    def __init__(self, args) -> None:
        self.args = args
        pygame.init()
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(S.TITLE)
        self.clock = pygame.time.Clock()
        self.frames = 0
        self.running = True

    def run(self) -> int:
        """Menjalankan siklus sampai jendela ditutup atau batas bingkai tiba."""
        while self.running:
            # Pengendali waktu: tick() membatasi laju bingkai sekaligus
            # memberitahu berapa lama bingkai sebelumnya berjalan.
            self.clock.tick(self.args.fps)

            # ---------- Tahap 1: membaca masukan ----------
            self.handle_events()

            # ---------- Tahap 2: memperbarui keadaan ----------
            # Belum ada keadaan yang berubah pada sesi ini.

            # ---------- Tahap 3: menayangkan ----------
            self.draw()
            pygame.display.flip()

            self.frames += 1
            if self.frames % 30 == 0:
                # Angka FPS terukur, bukan batas laju yang diminta, agar
                # perilaku program dapat diamati apa adanya.
                pygame.display.set_caption(
                    f"{S.TITLE} | {int(self.clock.get_fps())} FPS")

            if self.args.frames and self.frames >= self.args.frames:
                self.running = False
            if self.args.auto_close and self.frames >= 2:
                break

        pygame.quit()
        return 0

    def handle_events(self) -> None:
        """Menutup jendela atau menekan ESC mengakhiri program."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self) -> None:
        """Menggambar latar polos tanpa pemain."""
        self.screen.fill(S.BACKGROUND)

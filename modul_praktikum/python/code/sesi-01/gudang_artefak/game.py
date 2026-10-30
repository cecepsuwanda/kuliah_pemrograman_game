"""Jendela permainan Gudang Artefak.

Sesi 1 belum memakai siklus permainan. Program membuka jendela, mengisi
latarnya satu kali, lalu menunggu sampai jendela ditutup.
"""

from __future__ import annotations

import pygame

from . import settings as S


class Game:
    """Memegang jendela dan menjalankan perulangan peristiwa."""

    def __init__(self, args) -> None:
        self.args = args
        pygame.init()
        self.screen = pygame.display.set_mode((args.width, args.height))
        pygame.display.set_caption(S.TITLE)
        self.running = True
        print(f"Jendela {args.width}x{args.height} dibuka.")

    def run(self) -> int:
        self.screen.fill(S.BACKGROUND)
        pygame.display.flip()
        if getattr(self.args, "auto_close", False):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        while self.running:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
        pygame.quit()
        print("Program selesai.")
        return 0

"""Titik masuk permainan Gudang Artefak.

Jalankan dari folder sesi:
    python main.py
    python main.py --width 800 --height 600
"""

from __future__ import annotations

import argparse
import sys

from gudang_artefak.game import Game


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gudang Artefak")
    parser.add_argument("--width", type=int, default=960,
                        help="lebar jendela dalam piksel")
    parser.add_argument("--height", type=int, default=600,
                        help="tinggi jendela dalam piksel")
    parser.add_argument("--auto-close", action="store_true",
                        help="mengirim sendiri peristiwa QUIT untuk pengujian")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    game = Game(args)
    return game.run()


if __name__ == "__main__":
    sys.exit(main())

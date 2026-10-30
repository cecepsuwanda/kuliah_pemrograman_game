"""Titik masuk permainan Gudang Artefak.

Jalankan dari folder sesi:
    python main.py
    python main.py --level 2 --scenario 2
    python main.py --frames 120        (berhenti otomatis, untuk uji)
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
    parser.add_argument("--fps", type=int, default=60,
                        help="batas laju bingkai")
    parser.add_argument("--level", type=int, choices=(1, 2), default=1,
                        help="level yang dimulai lebih dahulu")
    parser.add_argument("--scenario", type=int, choices=(1, 2, 3), default=1,
                        help="peta Lorong untuk skenario uji")
    parser.add_argument("--frames", type=int, default=0,
                        help="berhenti otomatis setelah N bingkai (0 = tidak)")
    parser.add_argument("--auto-close", action="store_true",
                        help="langsung berhenti setelah dua bingkai")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    game = Game(args)
    game.start_level(args.level)
    return game.run()


if __name__ == "__main__":
    sys.exit(main())

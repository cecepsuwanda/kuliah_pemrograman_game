#!/usr/bin/env python3
"""Menampilkan letak kurung kurawal yang tidak berpasangan pada sebuah berkas.

Dipakai untuk menelusuri kerusakan berkas akibat penyuntingan otomatis.
Bagian di dalam lingkungan kodekeluaran dilewati karena bersifat verbatim.

Pemakaian:
    python -I scripts/periksa_kurung.py chapters/03/section-05.tex
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RE_KELUARAN = re.compile(
    r"\\begin\{kodekeluaran\}.*?\\end\{kodekeluaran\}", re.DOTALL
)
# Komentar LaTeX: tanda % yang berada di awal baris atau didahului spasi.
# Tanda % di dalam URL (misalnya %20) tidak dianggap komentar.
RE_KOMENTAR = re.compile(r"(?:(?<=\s)|^)%.*")


def periksa(nama: str) -> int:
    path = Path(nama)
    isi = path.read_text(encoding="utf-8")

    # Ganti blok keluaran dengan baris kosong agar nomor baris tetap sejajar.
    def ganti(cocok: re.Match[str]) -> str:
        return re.sub(r"[^\n]", "", cocok.group(0))

    isi = RE_KELUARAN.sub(ganti, isi)
    isi = "\n".join(RE_KOMENTAR.sub("", baris) for baris in isi.splitlines())

    tumpukan: list[tuple[int, int]] = []
    masalah: list[str] = []

    for nomor, baris in enumerate(isi.splitlines(), start=1):
        posisi = 0
        while posisi < len(baris):
            huruf = baris[posisi]
            if huruf == "\\" and posisi + 1 < len(baris):
                posisi += 2
                continue
            if huruf == "{":
                tumpukan.append((nomor, posisi))
            elif huruf == "}":
                if tumpukan:
                    tumpukan.pop()
                else:
                    masalah.append(
                        f"  baris {nomor}, kolom {posisi + 1}: '}}' tanpa "
                        f"'{{' pasangannya\n      {baris.strip()[:100]}"
                    )
            posisi += 1

    for nomor, posisi in tumpukan:
        masalah.append(
            f"  baris {nomor}, kolom {posisi + 1}: '{{' belum ditutup"
        )

    print(f"=== {nama} ===")
    if masalah:
        print(f"ditemukan {len(masalah)} kurung tidak berpasangan:")
        for satu in masalah:
            print(satu)
    else:
        print("kurung kurawal seimbang")
    return len(masalah)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    total = 0
    for nama in sys.argv[1:]:
        total += periksa(nama)
        print()
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

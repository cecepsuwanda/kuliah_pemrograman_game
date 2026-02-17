# Buku Ajar: Pemrograman Game Menggunakan Unity

Struktur:
- `main.tex`: berkas utama untuk membangun buku penuh (PDF).
- `chapters/*.tex`: setiap bab yang dapat dikompilasi mandiri memakai paket `subfiles`.
- `references.bib`: daftar pustaka (open access, dokumentasi resmi).
- `Makefile`: perintah membangun buku penuh dan per-bab.

Membangun:
```bash
# Bangun buku penuh
make -C buku-ajar-unity book

# Bangun salah satu bab (mis. 03)
make -C buku-ajar-unity 03-gameobject-komponen.pdf
```

Prasyarat: `latexmk`, `biber`.

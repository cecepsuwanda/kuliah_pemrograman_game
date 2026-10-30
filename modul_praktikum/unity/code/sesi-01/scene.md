# Checkpoint Sesi 01 — Scene Pertama

Project: **GudangArtefak** (2D, Unity LTS)
Scene: `Assets/Scenes/LevelRak.unity`

## Hierarchy yang diharapkan

```
LevelRak
├── Kamera
├── Gudang
│   ├── Lantai
│   ├── RakKiri
│   ├── RakTengah
│   ├── RakKanan
│   ├── Pemain
│   └── Pintu
└── CobaSkrip
```

## Komponen dan nilai inspector

| GameObject | Komponen | Nilai yang diisi |
|---|---|---|
| Kamera | Transform | Position (0, 0, -10) |
| Kamera | Camera | Projection: Orthographic; Size: 5; Background: #18203A |
| Gudang | Transform | Position (0, 0, 0) |
| Lantai | Sprite Renderer | Sprite: Square; Color: #46587E; Draw Mode: Tiled; Size (16, 1) |
| Lantai | Transform | Position (0, -3.5, 0); Scale (1, 1, 1) |
| RakKiri | Sprite Renderer | Sprite: Square; Color: #60749E; Size (3, 0.4) |
| RakKiri | Transform | Position (-4, -1.8, 0) |
| RakTengah | Sprite Renderer | Sprite: Square; Color: #60749E; Size (3, 0.4) |
| RakTengah | Transform | Position (0.5, -0.4, 0) |
| RakKanan | Sprite Renderer | Sprite: Square; Color: #60749E; Size (3, 0.4) |
| RakKanan | Transform | Position (4.5, -1.8, 0) |
| Pemain | Sprite Renderer | Sprite: Square; Color: #2E75B6; Size (0.8, 0.8) |
| Pemain | Transform | Position (-6.5, -3, 0) |
| Pintu | Sprite Renderer | Sprite: Square; Color: #3CA06E; Size (1, 2) |
| Pintu | Transform | Position (7, -2.6, 0) |
| CobaSkrip | Sprite Renderer | Sprite: Square; Color: #DEB242; Size (0.6, 0.6) |
| CobaSkrip | Transform | Position (0, 1.5, 0) |
| CobaSkrip | SkripPertama | Move Speed: 3; Turn Speed: 60; Report Interval: 2 |

Catatan: seluruh benda memakai sprite bawaan Unity (`Square`), bukan berkas
gambar. Warna diisi pada Sprite Renderer.

## Cara memeriksa

1. Tekan **Play**. `CobaSkrip` bergerak dengan tombol panah dan berputar.
2. Jendela **Console** menampilkan "Skrip mulai..." dan laporan setiap dua detik.
3. Hentikan Play. Perubahan posisi tidak tersimpan, dan Console menampilkan
   "Skrip berhenti...".

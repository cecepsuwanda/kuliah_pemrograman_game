# Checkpoint Sesi 02 — Level Rak dengan Tilemap dan Fisika

Project: **GudangArtefak** (2D, Unity LTS)
Scene: `Assets/Scenes/LevelRak.unity`

## Hierarchy yang diharapkan

```
LevelRak
├── Kamera
└── Gudang
    ├── Grid
    │   ├── TilemapLantai
    │   └── TilemapRak
    ├── Pemain
    │   └── TitikTanah
    ├── Artefak1
    ├── Artefak2
    ├── Artefak3
    └── Pintu
```

## Komponen dan nilai inspector

| GameObject | Komponen | Nilai yang diisi |
|---|---|---|
| Kamera | Transform | Position (0, 0, -10) |
| Kamera | Camera | Projection: Orthographic; Size: 5; Background: #18203A |
| Grid | Grid | Cell Size (1, 1, 0) |
| TilemapLantai | Tilemap, Tilemap Renderer | Petak x = -9 sampai 9 pada y = -4 |
| TilemapLantai | Tilemap Collider 2D | Used By Composite: dicentang |
| TilemapLantai | Composite Collider 2D | Geometry Type: Polygons |
| TilemapLantai | Rigidbody2D | Body Type: Static |
| TilemapLantai | Layer | Ground |
| TilemapRak | Tilemap, Tilemap Renderer | Tiga rak selebar empat petak: x = -6..-3 dan x = 4..7 pada y = -2; x = -1..2 pada y = 0 |
| TilemapRak | Tilemap Collider 2D | Used By Composite: dicentang |
| TilemapRak | Composite Collider 2D | Geometry Type: Polygons |
| TilemapRak | Rigidbody2D | Body Type: Static |
| TilemapRak | Layer | Ground |
| Pemain | Transform | Position (-6.5, -3, 0) |
| Pemain | Sprite Renderer | Sprite: Square; Color: #2E75B6; Size (0.8, 0.8) |
| Pemain | Tag | Player |
| Pemain | Rigidbody2D | Gravity Scale: 2.5; Collision Detection: Continuous; Interpolate: Interpolate; Constraints: Freeze Rotation Z |
| Pemain | Capsule Collider2D | Direction: Vertical; Size (0.7, 0.9) |
| Pemain | KontrolPemain | Move Speed 6; Jump Speed 11; Ground Radius 0.15; Ground Layer: Ground; Ground Check: TitikTanah |
| TitikTanah | Transform | Local Position (0, -0.5, 0) |
| Artefak1 | Transform | Position (-4, -1.1, 0) |
| Artefak1 | Sprite Renderer | Sprite: Square; Color: #DEB242; Size (0.5, 0.5) |
| Artefak1 | Circle Collider2D | Radius 0.25; Is Trigger: dicentang |
| Artefak1 | Artefak | Nilai 1; Player Tag: Player |
| Artefak2 | Transform | Position (1, 0.9, 0) |
| Artefak2 | Circle Collider2D | Radius 0.25; Is Trigger: dicentang |
| Artefak2 | Artefak | Nilai 1 |
| Artefak3 | Transform | Position (6, -1.1, 0) |
| Artefak3 | Circle Collider2D | Radius 0.25; Is Trigger: dicentang |
| Artefak3 | Artefak | Nilai 1 |
| Pintu | Transform | Position (8.3, -2.6, 0) |
| Pintu | Sprite Renderer | Sprite: Square; Color: #3CA06E; Size (1, 2) |
| Pintu | Box Collider2D | Size (1, 1.8); Is Trigger: dicentang |
| Pintu | Pintu | Artefak Diperlukan 3; Player Tag: Player |

Catatan: benda diam (tilemap dan artefak) tidak diberi Rigidbody2D dinamis.
Rigidbody2D pada tilemap berasal dari Composite Collider 2D dan bertipe Static.

## Cara memeriksa

1. Tekan **Play**. Pemain jatuh dan berhenti di atas lantai.
2. Gerakkan dengan tombol panah atau A/D. Pemain berjalan mendatar.
3. Tekan **Space** saat menyentuh tanah. Pemain melompat dan mendarat kembali.
4. Sentuh ketiga artefak. Ketiganya lenyap, dan Console mencatat
   "Artefak diambil. Total 1/2/3 artefak."
5. Sebelum artefak lengkap, masuki daerah pintu. Console mencatat
   "Pintu terkunci. Artefak n dari 3."
6. Setelah ketiga artefak diambil, masuki pintu. Console mencatat
   "Pintu terbuka. Level selesai."
7. Pilih Pemain pada tampilan Scene. Lingkaran hijau pemeriksaan tanah tampak
   di bawah kakinya.

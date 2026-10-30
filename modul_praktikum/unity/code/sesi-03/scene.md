# Checkpoint Sesi 03 — Aset, Animasi, dan HUD

Project: **GudangArtefak** (2D, Unity LTS)
Scene: `Assets/Scenes/LevelRak.unity`

## Hierarchy yang diharapkan

```
LevelRak
├── Kamera
├── Gudang
│   ├── Grid
│   │   ├── TilemapLantai
│   │   └── TilemapRak
│   ├── Pemain
│   │   └── TitikTanah
│   ├── Artefak1
│   ├── Artefak2
│   ├── Artefak3
│   └── Pintu
└── Canvas
    ├── TextSkor
    ├── TextNyawa
    ├── IkonNyawa1
    ├── IkonNyawa2
    └── IkonNyawa3
```

## Komponen dan nilai inspector

| GameObject | Komponen | Nilai yang diisi |
|---|---|---|
| Pemain | Sprite Renderer | Sprite: bingkai diam dari lembar pemain |
| Pemain | Rigidbody2D | Gravity Scale 2.5; Continuous; Interpolate; Freeze Rotation Z |
| Pemain | Capsule Collider2D | Direction: Vertical; Size (0.7, 0.9) |
| Pemain | Animator | Controller: AnimatorPemain; Parameters: speed (Float), grounded (Bool), lompat (Trigger) |
| Pemain | KontrolPemain | Move Speed 6; Jump Speed 11; Ground Radius 0.15; Ground Layer: Ground; Ground Check: TitikTanah; Animator: komponen Animator |
| Pemain | AnimasiPemain | Body: Rigidbody2D pemain; Ambang Gerak 0.1 |
| Canvas | Canvas | Render Mode: Screen Space - Overlay |
| Canvas | Canvas Scaler | UI Scale Mode: Scale With Screen Size; Reference Resolution 1920 x 1080; Match 0.5 |
| Canvas | TampilanHud | Score Text: TextSkor; Lives Text: TextNyawa; Heart Icons: 3 (IkonNyawa1--3) |
| TextSkor | Text | Anchor kiri atas; Pos (30, -30); Size 400 x 60; Font Size 36; Color putih; Text "Skor: 0" |
| TextNyawa | Text | Anchor kanan atas; Pos (-30, -30); Size 300 x 60; Font Size 36; Color putih; Text "Nyawa: 3" |
| IkonNyawa1 | Image | Anchor kanan atas; Pos (-30, -80); Size 32 x 32; Color #D94A4A |
| IkonNyawa2 | Image | Anchor kanan atas; Pos (-70, -80); Size 32 x 32; Color #D94A4A |
| IkonNyawa3 | Image | Anchor kanan atas; Pos (-110, -80); Size 32 x 32; Color #D94A4A |
| Artefak1--3 | Artefak | Nilai 1; Hud: Canvas |
| Pintu | Pintu | Artefak Diperlukan 3 |

## Keadaan Animator

| Keadaan | Animation clip | Keterangan |
|---|---|---|
| Idle | Idle | Keadaan bawaan (Set as Layer Default State) |
| Run | Run | Aktif ketika speed > 0.1 |
| Jump | Jump | Dipicu parameter lompat |

| Transisi | Syarat | Has Exit Time |
|---|---|---|
| Idle -> Run | speed Greater 0.1 | Tidak |
| Run -> Idle | speed Less 0.1 | Tidak |
| Any State -> Jump | lompat (Trigger) | Tidak |
| Jump -> Idle | grounded = true | Tidak |

## Pengaturan impor

| Aset | Sprite Mode | Pixels Per Unit | Filter Mode | Compression |
|---|---|---|---|---|
| Pemain (lembar animasi) | Multiple | 64 | Point | None |
| Petak lantai dan rak | Single | 64 | Point | None |
| Artefak | Single | 64 | Point | None |
| Pintu | Single | 64 | Point | None |

Nilai 64 dipakai karena bingkai contoh berukuran 64 x 64 piksel dan tinggi
pemain yang dikehendaki sekitar 1 satuan. Bila ukuran berkas berbeda, hitung
PPU = tinggi berkas / tinggi yang dikehendaki, lalu samakan untuk seluruh aset.

## Cara memeriksa

1. Tekan **Play**. Pemain menampilkan animasi diam.
2. Gerakkan pemain. Animasi berlari muncul, dan gambar menghadap sesuai arah
   gerak.
3. Tekan **Space**. Animasi melompat muncul sekali, lalu kembali diam setelah
   mendarat.
4. Ambil ketiga artefak. TextSkor berubah menjadi "Skor: 3".
5. Hentikan Play sementara, klik kanan komponen **TampilanHud**, pilih
   **Uji kurangi satu nyawa**. TextNyawa menjadi "Nyawa: 2" dan satu ikon
   lenyap.
6. Periksa Console: tidak ada pesan merah, dan skor tercatat setiap artefak
   diambil.

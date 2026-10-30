# Checkpoint Sesi 04 — Audio dan Trigger Interaksi

Project: **GudangArtefak** (2D, Unity LTS)
Scene: `Assets/Scenes/LevelRak.unity`

## Hierarchy yang diharapkan

```
LevelRak
├── Kamera
├── ManajerBunyi
├── Gudang
│   ├── Grid
│   │   ├── TilemapLantai
│   │   └── TilemapRak
│   ├── Pemain
│   │   └── TitikTanah
│   ├── Artefak1
│   ├── Artefak2
│   ├── Artefak3
│   ├── PartikelAmbil1        (opsional)
│   ├── PartikelAmbil2        (opsional)
│   ├── PartikelAmbil3        (opsional)
│   └── Pintu
└── Canvas
    ├── TextSkor
    ├── TextNyawa
    ├── IkonNyawa1
    ├── IkonNyawa2
    └── IkonNyawa3
```

`ManajerBunyi` diletakkan di akar scene, bukan di bawah `Gudang`, agar tidak
ikut mati apabila level dimuat ulang.

## Komponen dan nilai Inspector

| GameObject | Komponen | Nilai yang diisi |
|---|---|---|
| ManajerBunyi | ManajerBunyi | Music Source: AudioSource 1; Sfx Source: AudioSource 2; Musik Latar: `musik-gudang`; Bunyi Lompat: `lompat`; Bunyi Ambil: `ambil`; Bunyi Kalah: `kalah`; Volume Musik 0.4; Volume Efek 0.8; Variasi Nada 0.08 |
| ManajerBunyi | AudioSource 1 | Play On Awake: tidak; Loop: ya; Spatial Blend: 0; Output: Mixer `Gudang` > `Musik`; Volume 0.4 |
| ManajerBunyi | AudioSource 2 | Play On Awake: tidak; Loop: tidak; Spatial Blend: 0; Output: Mixer `Gudang` > `Efek`; Volume 0.8 |
| Pemain | KontrolPemain | Pemicu Bunyi: komponen PemicuBunyi pada Pemain |
| Pemain | PemicuBunyi | Manajer: objek ManajerBunyi |
| Canvas | TampilanHud | Pemicu Bunyi: komponen PemicuBunyi pada Pemain |
| Artefak1--3 | Artefak | Nilai 1; Hud: Canvas; Pemicu Bunyi: komponen PemicuBunyi pada Pemain; Partikel Ambil: PartikelAmbil1--3 (opsional) |
| PartikelAmbil1--3 | Particle System | Looping: tidak; Play On Awake: tidak; Start Lifetime 0.4; Start Speed 2; Burst 12 partikel |
| Pintu | Pintu | Artefak Diperlukan 3 |

## Berkas bunyi dan pengaturannya

| Berkas | Keperluan | Load Type | Compression | Lisensi |
|---|---|---|---|---|
| `musik-gudang` | BGM, berulang | Streaming | Vorbis | dicatat pada Lembar Kerja |
| `lompat` | SFX lompat | Decompress On Load | PCM | dicatat pada Lembar Kerja |
| `ambil` | SFX artefak diambil | Decompress On Load | PCM | dicatat pada Lembar Kerja |
| `kalah` | SFX nyawa habis | Decompress On Load | PCM | dicatat pada Lembar Kerja |

Nama berkas di atas adalah contoh. Sesuaikan dengan berkas yang Anda unduh,
lalu catat sumber dan lisensinya.

## AudioMixer

| Tingkat | Volume awal | Keluaran |
|---|---|---|
| Master | 0 dB | AudioListener |
| Musik | -8 dB | Master |
| Efek | 0 dB | Master |

Kedua AudioSource diarahkan ke tingkat yang sesuai melalui
**Output** pada komponen AudioSource.

## Daftar peristiwa dan bunyi

| Peristiwa | Bunyi | Jenis | Dipanggil oleh | Pasangan yang terlihat |
|---|---|---|---|---|
| Scene dimulai | `musik-gudang` | BGM | `ManajerBunyi.Start` | Level langsung terlihat dan dapat dimainkan |
| Tombol lompat ditekan | `lompat` | SFX | `KontrolPemain.Update` | Animasi lompat dan posisi pemain naik |
| Artefak tersentuh | `ambil` | SFX | `Artefak.OnTriggerEnter2D` | Skor bertambah, artefak lenyap, partikel (opsional) |
| Nyawa mencapai nol | `kalah` | SFX | `TampilanHud.KurangiNyawa` | Teks nyawa menjadi 0 dan ikon nyawa lenyap |
| Pemain mencapai pintu | tidak ada | — | `Pintu.OnTriggerEnter2D` | Pesan pada Console |

## Cara memeriksa

1. Tekan **Play**. Musik latar terdengar sejak awal dan berulang setelah
   selesai.
2. Tekan **Space**. Bunyi lompat terdengar seketika, bersamaan dengan animasi
   lompat.
3. Ambil ketiga artefak. Setiap pengambilan berbunyi dan skor bertambah.
4. Hentikan Play, klik kanan komponen **TampilanHud**, pilih
   **Uji kurangi satu nyawa** tiga kali. Pada nyawa ketiga, musik berhenti dan
   bunyi kalah terdengar.
5. Periksa Console: tidak ada pesan merah dan tidak ada peringatan rujukan
   kosong.
6. Ubah **Volume Musik** menjadi 0.15 lalu jalankan kembali. Pastikan efek suara
   masih terdengar di atas musik.

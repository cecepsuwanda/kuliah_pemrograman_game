# Peta Rujukan per Bab

Dokumen kerja untuk penulisan bab. Menghubungkan setiap bab buku ajar dengan
bagian konkret pada tiga buku referensi yang sudah diekstrak di `referensi/`,
ditambah nomor rujukan `[R1]`–`[R35]` yang sama dengan RPS.

## 1. Isi dan letak bagian pada tiga buku referensi

Ketiga PDF diekstrak halaman per halaman dengan tata letak yang sama:

| Berkas | Isi |
|---|---|
| `<buku>.tex` | Gabungan seluruh halaman, tanpa penanda `\chapter` |
| `pages/llm/page_NNN.tex` | Satu dokumen LaTeX per halaman PDF |
| `images/llm/` | **Potongan gambar yang benar-benar dirujuk** oleh berkas `.tex` |
| `images/python/` | Raster hasil ekstraksi mentah, **tidak dirujuk** berkas mana pun |
| `renders/page_NNN.png` | Raster halaman penuh, dipakai sebagai kanvas koordinat |
| `crops.json` | Kotak gambar per halaman + `deskripsi` berbahasa Indonesia |

**Aturan pakai gambar: hanya dari `images/llm/`.** Direktori `images/python/`
adalah hasil samping proses ekstraksi (versi mentah, ikon lisensi) dan tidak
dipakai buku mana pun. Keterangan gambar diambil dari `deskripsi` pada
`crops.json` atau dari kalimat `Figure X-Y: ...` di badan teks halaman.

### 1.1 Making Games with Python & Pygame (Al Sweigart)

Tulang punggung utama materi 1–9 karena seluruhnya berbasis Pygame.

| Bab | Pokok bahasan | Halaman |
|---|---|---|
| Ch 1 | Installing Python and Pygame | 019–024 |
| **Ch 2** | **Pygame Basics** | **025–050** |
| Ch 3 | Memory Puzzle | 051–094 |
| Ch 4 | Slide Puzzle | 095–125 |
| Ch 5 | Simulate | 126–148 |
| Ch 6 | Wormy (gerak grid, tabrakan) | 149–170 |
| Ch 7 | Tetromino (waktu, jatuh, rotasi) | 171–217 |
| **Ch 8** | **Squirrel Eat Squirrel** (pemain, musuh, pantulan) | **218–259** |
| Ch 9 | Star Pusher (peta berhalangan, data level) | 260–306 |
| Ch 10 | Four Extra Games (Flippy, Ink Spill, Four-in-a-Row, Gemgem) | 307–359 |
| — | Glosarium | 360–363 |

### 1.2 Invent Your Own Computer Games with Python (Al Sweigart)

Referensi kedua. Hanya Bab 17–20 yang membahas grafik; sisanya permainan teks.

| Bab | Pokok bahasan | Halaman |
|---|---|---|
| Ch 1 | Installing Python | 027–033 |
| Ch 16 | AI Simulation (metrik, simulasi) | 333–349 |
| **Ch 17** | **Graphics and Animation (Pygame)** | **350–380** |
| **Ch 18** | **Collision Detection and Input** | **381–403** |
| **Ch 19** | **Sound and Images** (`pygame.mixer`) | **404–414** |
| Ch 20 | Dodger (permainan lengkap) | 415–445 |

### 1.3 Unity — Introduction to Level Design (2022 LTS)

| Bagian | Pokok bahasan | Halaman |
|---|---|---|
| Part I | Praproduksi, 3C (camera, character, control), metrik, white-boxing, jalur pemain, *signposting*, suara, checkpoint, pengujian otomatis | 009–039 |
| **Part II** | Instal Unity, Unity Editor, Package Manager, GameObject, Scene view, tag, prefab | 040–053 |
| Part II | Dasar C\#, membuat script | 054–057 |
| **Part II** | **Visual Scripting dan State Machine (State Graph)** | **058–061** |
| **Part II** | **Physics: collider, rigidbody, trigger, layer, refresh rate** | **062–068** |
| **Part II** | **Animation window, Animation State Machine, Timeline** | **069–073** |
| Part III | Starter assets, ProBuilder, Polybrush, Splines, Terrain | 074–102 |
| Part III | 2D Tilemap | 103–104 |
| **Part III** | **Pathfinding dengan AI Navigation (NavMesh)** | **108–111** |

## 2. Rujukan per bab

`Sumber utama` = bahan untuk menulis materi. `[Rn]` = nomor rujukan pada
daftar pustaka buku (sama dengan RPS). Nomor halaman merujuk berkas
`pages/llm/page_NNN.tex` pada direktori buku referensi terkait.

| Bab | Sumber utama (halaman) | Rujukan | Gambar tersedia |
|---|---|---|---|
| I Pendahuluan | RPS `rps/sections/01`–`04` | — | — |
| II Landasan Teori | mg 025–027 (Pygame Basics); unity 009–023 (3C, metrik) | [R5], [R12], [R13] | unity 015–018, 024–027 |
| III Materi 1 | iwp 027–033; mg 019–024 | [R1], [R2], [R20], [R21] | mg 021, iwp 029 |
| IV Materi 2 | **mg 025–050** (paling lengkap) | [R3], [R5], [R6], [R22] | mg 026, 029, 034, 038 |
| V Materi 3 | iwp 366–380; mg 095–125, 171–217 | [R3], [R32], [R1] | mg 038–044 |
| VI Materi 4 | mg 218–259 (pantulan, sinus); iwp 415–445 (Dodger) | [R7], [R22], [R1] | mg 228, 233 |
| VII Materi 5 | mg 051–094, 149–170; **iwp 381–403** | [R4], [R23], [R21] | iwp 385–400, mg 140–142 |
| VIII Materi 6 | mg 218–241 (musuh mendekati pemain); iwp 179–216, 293–332 | [R1], [R2], [R19], [R33] | mg 229–241 |
| IX Materi 7 | **unity 058–061** (State Graph); unity 069–073 | [R9], [R25], [R27] | unity 058–061 |
| X Materi 8 | **unity 108–111** (NavMesh); mg 260–306 (peta data) | [R8], [R10], [R11], [R34] | unity 108–111 |
| XI Materi 9 | unity 061 + 108–111; mg 260–306 | [R8], [R9], [R25], [R26] | unity 061, 108–111 |
| XII Materi 10 | **unity 040–053** | [R12], [R13], [R15], [R16] | unity 042, 045–053 |
| XIII Materi 11 | **unity 062–068, 074–104** | [R12], [R13], [R18], [R35] | unity 063, 066–067, 077–097 |
| XIV Materi 12 | **unity 069–073**; mg 025–050 (teks) | [R12], [R14], [R28], [R29] | unity 070–073 |
| XV Materi 13 | **iwp 404–414** (`pygame.mixer`); unity 035 | [R14], [R24], [R30], [R31] | iwp 404, 412 |
| XVI Materi 14 | **unity 036–039** (pengujian); iwp 333–349 | [R12], [R16], [R18], [R30] | unity 039 |
| XVII Evaluasi | RPS `rps/sections/08`, `09` | — | — |

Keterangan: `iwp` = `referensi/inventwithpython`, `mg` = `referensi/makinggames`,
`unity` = `referensi/UNITY_Ebook_Introduction to level design ...`.

## 3. Materi yang harus ditulis sendiri (tidak ada pada ketiga PDF)

Pemeriksaan isi menunjukkan beberapa topik mata kuliah ini **tidak dibahas**
pada ketiga buku referensi. Topik tersebut ditulis sendiri dengan bersandar
pada dokumentasi resmi dan bahan kuliah pada `[R3]`, `[R4]`, `[R7]`, `[R8]`,
`[R10]`, `[R11]`, dan `[R34]`:

| Topik | Bab | Sumber pengganti |
|---|---|---|
| `pygame.Vector2` | V | [R3] dokumentasi API Pygame |
| `delta time` (`clock.tick()` sebagai selang waktu) | V | [R3], [R6] |
| Gravitasi dan impuls lompatan yang eksplisit | VI | [R7] integrasi numerik, [R22] |
| Kelas `pygame.sprite.Sprite`, `Group`, `spritecollide`, `groupcollide` | VII | [R4] dokumentasi sprite |
| Algoritma A\* dari sisi algoritmik (bukan NavMesh) | X | [R11], [R10], [R34], [R8] |
| FSM sebagai kelas Python (bukan State Graph Unity) | IX | [R9], [R25], [R27] |

Untuk materi Unity, `unity 040–111` sudah memadai, ditambah materi Python
yang sudah dipahami mahasiswa sebagai pembanding konsep.

## 4. Catatan mutu ekstraksi

Rata-rata tumpang tindih teks antara hasil ekstraksi LLM dan hasil ekstraksi
Python: `inventwithpython` 0,76; `makinggames` 0,57; Unity 0,82. Artinya teks
`makinggames` paling kurang akurat. Setiap kutipan **wajib diperiksa ulang
pada `renders/page_NNN.png`** sebelum dipakai, dan penulisan bab tetap
menggunakan kalimat sendiri, bukan menyalin.

## 5. Atribusi gambar

Setiap gambar dari referensi diberi keterangan sumber di bawah gambar:

```latex
\sumber{[R12] hal. 63}
```

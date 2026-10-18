# Buku Ajar Pengantar Pemrograman Game (MWCA009)

Buku ajar LaTeX untuk mata kuliah **Pengantar Pemrograman Game**
(kode **MWCA009**, 3 SKS) Program Studi Teknik Informatika, Fakultas Teknologi
Informasi, Universitas Bale Bandung. Isi buku mengikuti
Rencana Pembelajaran Semester (RPS) berbasis *Outcome-Based Education* (OBE)
yang tersimpan pada folder `rps/`.

## Cara Membangun

Membangun seluruh buku:

```bat
scripts\build-all.bat
```

atau langsung:

```bash
latexmk -pdf main.tex
```

Membangun satu bab (menghasilkan PDF bab tersendiri):

```bat
scripts\build-chapter.bat 04
```

Membersihkan berkas bantu (PDF tetap disimpan):

```bat
scripts\clean.bat
```

Memeriksa konsistensi proyek (kelengkapan berkas, cakupan Sub-CPMK,
kesesuaian sitasi, label, gambar, dan berkas kode):

```bash
python -I scripts/periksa_buku.py
```

Keluaran seluruh buku: **`main.pdf`**. Keluaran satu bab:
`chapters/XX/chapter.pdf`.

## Struktur Direktori

```text
buku_ajar/
├── main.tex                  dokumen induk (front matter, bab, lampiran, pustaka)
├── preamble.tex              pemanggil konfigurasi
├── metadata.tex              identitas buku, mata kuliah, dan institusi
├── references.tex            daftar pustaka [R1]--[R35]
├── PETA_RUJUKAN.md           peta sumber materi per bab (dokumen kerja)
├── README.md                 berkas ini
│
├── config/
│   ├── packages.tex          seluruh paket LaTeX
│   ├── styles.tex            warna, tipe kolom, format judul, header/footer
│   ├── commands.tex          identitas, perintah khusus, akar direktori kode/aset
│   ├── environments.tex      kotak OBE (tujuan, Sub-CPMK, praktikum, checklist, …)
│   └── listings.tex          konfigurasi kode Python dan C#
│
├── frontmatter/              halaman judul, hak cipta, kata pengantar,
│                             petunjuk penggunaan, capaian pembelajaran
│
├── chapters/01 … 17/         bab; tiap bab adalah unit kompilasi mandiri
│   ├── chapter.tex           pemanggil bab (subfiles)
│   ├── sub-cpmk.tex          Sub-CPMK, indikator, ranah Bloom
│   ├── tujuan.tex            tujuan pembelajaran bab
│   ├── section-01 … NN.tex   materi pokok
│   ├── contoh.tex            contoh dan ilustrasi
│   ├── praktikum.tex         aktivitas pembelajaran / lembar kerja
│   ├── latihan.tex           soal latihan dan refleksi
│   ├── rangkuman.tex         ringkasan bab
│   ├── checklist.tex         checklist pencapaian kompetensi
│   ├── evaluasi.tex          asesmen dan instrumen penilaian
│   └── figures/              gambar dan diagram TikZ khusus bab ini
│
├── appendices/               Lampiran A–D
├── assets/images/            gambar yang dipakai lebih dari satu bab
├── code/python/              kode Python (Materi 1–9)
├── code/unity/               skrip C# Unity (Materi 10–14)
└── scripts/                  skrip kompilasi dan pemeriksa konsistensi
```

Isi buku dipisahkan dari konfigurasi teknis: berkas pada `chapters/` hanya
memuat materi, sedangkan paket, gaya tampilan, dan definisi perintah berada
pada `config/`. Penambahan bab tidak menuntut perubahan pada bab lain.

## Peta Bab

| Bab | Judul | Materi RPS | Sub-CPMK |
|---|---|---|---|
| I | Pendahuluan dan Orientasi Buku | orientasi | — |
| II | Landasan Teori dan Konsep Dasar | fondasi | — |
| III | Pengantar Pemrograman Game dan Persiapan Lingkungan | 1 | menuju 1.1 |
| IV | *Game Loop*, *Event Handling*, dan *Clock* | 2 | 1.1 |
| V | Gerak Objek, `Vector2`, Input, dan *Delta Time* | 3 | 1.2 |
| VI | Fisika Sederhana: Gravitasi, Lompatan, dan Pantulan | 4 | 1.3 |
| VII | *Sprite*, *Group*, dan *Collision Detection* | 5 | 1.4 |
| VIII | Pengantar AI NPC dan Perilaku *Chase* | 6 | 2.1 |
| IX | *Finite State Machine* untuk NPC | 7 | 2.2 |
| X | *Pathfinding* Grid: dari BFS/Dijkstra ke A* | 8 | 2.3 |
| XI | Integrasi FSM dan A* (Mini Proyek AI) | 9 | 2.4 |
| XII | Pengenalan Unity: *Project*, *Scene*, *GameObject* | 10 | 3.1 |
| XIII | Membangun Level, *Physics*, dan Kontrol Pemain | 11 | 3.2 |
| XIV | Impor Aset Visual, Animasi, dan UI Dasar | 12 | 4.1 |
| XV | Integrasi Audio dan *Trigger* Interaksi | 13 | 4.2 |
| XVI | Evaluasi Prototipe, *Playtesting*, dan Presentasi | 14 | 4.3 |
| XVII | Evaluasi, Refleksi, dan Integrasi Kompetensi | penutup | 1.1–4.3 |

Bab diaktifkan satu per satu pada `main.tex` setelah selesai dan diperiksa.
Baris `\subfile{chapters/XX/chapter}` pada blok *MAIN MATTER* dibuka komentarnya
ketika bab yang bersangkutan sudah ditulis.

## Konvensi Penulisan

- **`\code{...}` aman terhadap garis bawah.** Perintah ini memakai
  `\detokenize`, sehingga ditulis apa adanya:

  ```latex
  benar : \code{pygame.key.get_pressed}   \code{code/python/ch04_game_loop.py}
  salah : \code{pygame.key.get\_pressed}
  ```

- **Istilah asing** memakai `\istilah{...}` (miring). Nama berkas, fungsi, dan
  potongan kode di dalam teks memakai `\code{...}`.

- **Gambar khusus bab** disimpan di `chapters/XX/figures/` dan dipanggil
  dengan `figures/nama.png`. **Gambar lintas bab** disimpan di
  `assets/images/` dan dipanggil dengan `\assetfile{images/nama.png}`.

- **Diagram** digambar dengan TikZ pada berkas `figures/nama.tikz` dan
  dipanggil dengan `\input{figures/nama.tikz}`.

- **Kode program** disimpan sebagai berkas nyata di `code/` dan dipanggil
  dengan `\kodepython{python/nama.py}{Judul}{lst:label}` atau
  `\kodecsharp{unity/Nama.cs}{Judul}{lst:label}`.

- **Sitasi** memakai `\cite{kunci}` dan tercetak sebagai `[R1]`–`[R35]`, sama
  dengan nomor rujukan pada RPS. Kunci pustaka didefinisikan pada
  `references.tex`.

- **Rujukan ke bab lain** memakai `\refbab{chap:slug}{Teks cadangan}`. Nomor
  bab dicetak bila labelnya tersedia; bila bab dikompilasi mandiri dan label
  belum ada, teks cadangan yang dicetak.

- **Gambar dari sumber lain** wajib diberi `\sumber{[R12] hal. 63}` di bawah
  gambar.

- **Label** memakai awalan `chap:`, `sec:`, `fig:`, `tab:`, `eq:`, `lst:`.

## Catatan Teknis

Beberapa keputusan berikut diambil setelah diuji pada instalasi LaTeX yang
dipakai (MiKTeX 24.1) dan berbeda dari `Arsitektur_Buku_Ajar.md`:

1. **`main.tex` memakai `\subfile`, bukan `\include`.** Paket `subfiles`
   memuat paket `import` yang menyetel `\input@path` dan `\Ginput@path` ke
   direktori bab. Tanpa itu, `\includegraphics{figures/...}` dan
   `\input{contoh}` gagal ditemukan ketika seluruh buku dikompilasi.

2. **`\ifSubfilesClassLoaded` menerima dua argumen berkurawal**, bukan
   kondisional `\if...\else...\fi`:

   ```latex
   \ifSubfilesClassLoaded{<bila bab dikompilasi mandiri>}{<bila seluruh buku>}
   ```

   Menulisnya sebagai `\if...\else...\fi` menghasilkan galat `Extra \else`
   dan nama berkas yang kacau.

3. **Kondisi tidak boleh berada di dalam argumen nama berkas**
   (`\includegraphics`, `\lstinputlisting`), karena argumen tersebut diproses
   ulang oleh `\edef`. Karena itu akar direktori ditentukan sekali pada
   `config/commands.tex` (`\coderoot`, `\assetroot`), lalu dipakai melalui
   `\codefile{...}` dan `\assetfile{...}`.

4. **`xr-hyper` dipakai, bukan `xr`.** Paket `xr` menimbulkan galat
   `\XR@prefix undefined` ketika `hyperref` dimuat.

5. **`colortbl` tidak dipakai** karena `array.sty` pada instalasi ini terlalu
   tua. Header tabel ditandai garis tebal melalui `\renewcommand{\toprule}`
   pada `config/styles.tex`, mengikuti pola `rps/config/styles.tex`.

6. **Kompilasi dilakukan di tempat** (berkas bantu berada di samping
   sumbernya), bukan ke direktori `build/`. Kompilasi bab mandiri bergantung
   pada path relatif `../../` sehingga direktori keluaran terpisah akan
   memutus rantai tersebut.

7. **Penutup kotak ditulis `\end{namabox}`, bukan `</namabox>`.** Bentuk
   bergaya HTML itu terketik berulang kali dan selalu menimbulkan galat
   `Not in outer par mode` yang menunjuk jauh dari penyebabnya (kotak tidak
   pernah ditutup, sehingga lingkungan berikutnya dianggap berada di dalam
   kotak). Pemeriksa `scripts/periksa_buku.py` kini memiliki aturan khusus
   untuk bentuk itu, di samping pemeriksaan keseimbangan `\begin`/`\end`
   yang tidak dapat melihatnya.

## Berkas Bantu dan Git

Berkas bantu LaTeX (`*.aux`, `*.log`, `*.toc`, `*.lof`, `*.lot`, `*.fls`,
`*.fdb_latexmk`, `*.out`, `*.bbl`, `*.blg`, `*.synctex.gz`) sudah tercakup
pada `.gitignore` di akar repositori dan tidak boleh ikut disimpan.

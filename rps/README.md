# RPS Pengantar Pemrograman Game (MWCA009)

Dokumen Silabus dan Rencana Pembelajaran Semester (RPS) berbasis
*Outcome-Based Education* (OBE) untuk mata kuliah **Pengantar Pemrograman Game**
(kode **MWCA009**, 3 SKS), Program Studi Teknik Informatika, Fakultas Teknologi
Informasi, Universitas Bale Bandung.

## Cara Membangun

```bat
cd rps
build.bat
```

atau langsung dengan `latexmk`:

```bash
latexmk -pdf rps.tex
```

Tanpa `latexmk` (jalankan dua kali agar daftar isi dan rujukan silang terisi):

```bash
pdflatex rps.tex
pdflatex rps.tex
```

Membersihkan berkas bantu (PDF tetap disimpan):

```bash
latexmk -c rps.tex
```

Keluaran: **`rps.pdf`** (31 halaman, A4).

## Struktur Direktori

```text
rps/
├── rps.tex                     dokumen induk (halaman judul + pemanggil bagian)
├── build.bat                   skrip kompilasi
├── README.md                   berkas ini
│
├── config/
│   ├── packages.tex            seluruh paket LaTeX
│   ├── styles.tex              warna, tipe kolom, format judul, header/footer
│   └── commands.tex            identitas mata kuliah dan perintah khusus
│
└── sections/
    ├── 01-identitas.tex        Bagian 1  Identitas Mata Kuliah
    ├── 02-cpl.tex              Bagian 2  Capaian Pembelajaran Lulusan (CPL)
    ├── 03-cpmk.tex             Bagian 3  Capaian Pembelajaran Mata Kuliah (CPMK)
    ├── 04-sub-cpmk.tex         Bagian 4  Sub-CPMK dan Indikator Pencapaian
    ├── 05-materi.tex           Bagian 5  Materi Pembelajaran (Bahan Kajian)
    ├── 06-metode.tex           Bagian 6  Metode Pembelajaran
    ├── 07-pengalaman-belajar.tex  Bagian 7  Pengalaman Belajar Mahasiswa
    ├── 08-penilaian.tex        Bagian 8  Kriteria, Indikator, dan Bobot Penilaian
    ├── 09-evaluasi-refleksi.tex   Bagian 9  Evaluasi dan Refleksi Pembelajaran
    ├── 10-referensi.tex        Bagian 10 Daftar Referensi
    └── 11-pengesahan.tex       Halaman pengesahan
```

Isi dokumen dipisahkan dari konfigurasi teknis: bagian pada `sections/` hanya
memuat materi, sedangkan paket, gaya tampilan, dan definisi perintah berada di
`config/`. Penambahan atau penyuntingan satu bagian tidak menuntut perubahan
pada bagian lain.

## Menyesuaikan Isi

Identitas mata kuliah (nama dosen, semester, tahun akademik, nama program
studi) didefinisikan sekali pada `config/commands.tex`, sehingga perubahan
otomatis berlaku pada seluruh dokumen.

Beberapa butir berikut perlu disesuaikan dengan ketentuan resmi program studi
apabila berbeda:

| Butir | Letak | Nilai saat ini |
|-------|-------|----------------|
| Bobot SKS | `sections/01-identitas.tex` | 3 SKS (2 SKS teori, 1 SKS praktikum) |
| Mata kuliah prasyarat | `sections/01-identitas.tex` | Algoritma dan Pemrograman |
| Bobot komponen penilaian | `sections/08-penilaian.tex` | Praktikum 25%, Kuis 10%, UTS 20%, Mini Proyek 10%, Proyek Akhir 30%, Partisipasi 5% |
| Konversi nilai huruf | `sections/08-penilaian.tex` | A >= 80, B 70--79, C 60--69, D 50--59, E < 50 |
| Nama Ketua Program Studi dan NIDN | `sections/11-pengesahan.tex` | masih berupa titik-titik |

## Catatan Teknis

- Opsi `[table]` pada `xcolor` (paket `colortbl`) **tidak** digunakan karena
  pada instalasi ini `colortbl` menuntut `array.sty` yang lebih baru
  (`\insert@pcolumn` tidak terdefinisi). Sebagai gantinya, header tabel
  ditandai dengan garis tebal di atas dan garis tipis di bawah
  (`config/styles.tex`). Cara mengaktifkan kembali latar baris tabel
  diuraikan pada komentar di `config/commands.tex`.
- Tabel rencana pembelajaran mingguan dan tabel rincian materi dicetak
  melintang (*landscape*) menggunakan paket `pdflscape` dengan huruf
  `\footnotesize` agar seluruh kolom muat dalam satu halaman.
- URL panjang dipenggal otomatis berkat paket `xurl`.

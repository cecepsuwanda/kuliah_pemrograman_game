# Arsitektur Final Buku Ajar LaTeX Modular

## 1. Tujuan

Arsitektur ini dirancang untuk membangun buku ajar menggunakan LaTeX dengan karakteristik:

1. Buku terdiri dari banyak bab.
2. Setiap bab dapat dikompilasi secara terpisah.
3. Seluruh bab dapat dikompilasi menjadi satu buku.
4. Konfigurasi LaTeX dikelola secara terpusat.
5. Materi bab dipisahkan dari konfigurasi teknis.
6. Setiap bab dapat dipecah menjadi beberapa section.
7. Gambar, kode program, latihan, dan evaluasi dapat dikelola secara modular.
8. Struktur dapat digunakan oleh editor maupun AI coding/writing assistant.
9. Penambahan bab baru tidak memerlukan perubahan besar pada struktur proyek.
10. Proyek tetap mudah dipelihara ketika jumlah bab mencapai 14–16 bab atau lebih.

---

# 2. Prinsip Arsitektur

Arsitektur menggunakan prinsip berikut:

```text
MASTER DOCUMENT
      │
      ├── Front Matter
      │
      ├── Chapters
      │      ├── Chapter 01
      │      ├── Chapter 02
      │      ├── Chapter 03
      │      └── ...
      │
      └── Back Matter
```

Konfigurasi dipisahkan:

```text
main.tex
   │
   └── preamble.tex
          │
          └── config/
                ├── packages.tex
                ├── commands.tex
                ├── environments.tex
                ├── styles.tex
                └── listings.tex
```

Prinsip utama:

> **Konten buku tidak boleh bercampur dengan konfigurasi teknis LaTeX.**

---

# 3. Struktur Direktori Final

Struktur yang direkomendasikan:

```text
book/
│
├── main.tex
├── preamble.tex
├── metadata.tex
├── references.bib
│
├── config/
│   ├── packages.tex
│   ├── commands.tex
│   ├── environments.tex
│   ├── styles.tex
│   └── listings.tex
│
├── frontmatter/
│   ├── cover.tex
│   ├── copyright.tex
│   ├── preface.tex
│   ├── acknowledgements.tex
│   └── learning-outcomes.tex
│
├── chapters/
│   │
│   ├── 01/
│   │   ├── chapter.tex
│   │   ├── section-01.tex
│   │   ├── section-02.tex
│   │   ├── section-03.tex
│   │   ├── contoh.tex
│   │   ├── praktikum.tex
│   │   ├── latihan.tex
│   │   ├── rangkuman.tex
│   │   ├── evaluasi.tex
│   │   └── figures/
│   │
│   ├── 02/
│   │   ├── chapter.tex
│   │   ├── section-01.tex
│   │   ├── section-02.tex
│   │   ├── contoh.tex
│   │   ├── praktikum.tex
│   │   ├── latihan.tex
│   │   ├── rangkuman.tex
│   │   ├── evaluasi.tex
│   │   └── figures/
│   │
│   ├── 03/
│   │   └── ...
│   │
│   └── 16/
│       └── ...
│
├── appendices/
│   ├── appendix-a.tex
│   └── appendix-b.tex
│
├── assets/
│   ├── images/
│   ├── diagrams/
│   └── logos/
│
├── code/
│   ├── cpp/
│   ├── python/
│   ├── pascal/
│   └── matlab/
│
├── build/
│
└── scripts/
    ├── build-all.bat
    ├── build-chapter.bat
    └── clean.bat
```

---

# 4. Fungsi Setiap Direktori

## 4.1 Root

```text
main.tex
preamble.tex
metadata.tex
references.bib
```

Berisi file utama proyek.

### `main.tex`

Merupakan master document.

Tugasnya:

- menentukan document class;
- memanggil konfigurasi;
- memanggil front matter;
- memanggil semua bab;
- memanggil appendix;
- memanggil bibliography.

`main.tex` sebaiknya tidak berisi materi pembelajaran.

---

### `preamble.tex`

Merupakan penghubung konfigurasi:

```latex
\input{config/packages}
\input{config/styles}
\input{config/commands}
\input{config/environments}
\input{config/listings}
```

---

### `metadata.tex`

Berisi metadata buku:

```latex
\newcommand{\BookTitle}{Judul Buku}
\newcommand{\BookAuthor}{Nama Penulis}
\newcommand{\BookEdition}{Edisi Pertama}
\newcommand{\BookYear}{2026}
\newcommand{\BookInstitution}{Nama Institusi}
```

Metadata tidak dicampur dengan materi bab.

---

### `references.bib`

Berisi seluruh referensi bibliografi.

Contoh:

```bibtex
@book{aho2006,
    author    = {Aho, Alfred V. and Lam, Monica S. and Sethi, Ravi and Ullman, Jeffrey D.},
    title     = {Compilers: Principles, Techniques, and Tools},
    publisher = {Pearson},
    year      = {2006}
}
```

---

# 5. `config/`

Direktori `config/` berisi konfigurasi teknis LaTeX.

Struktur:

```text
config/
├── packages.tex
├── commands.tex
├── environments.tex
├── styles.tex
└── listings.tex
```

---

## 5.1 `packages.tex`

Semua package didefinisikan di sini.

Contoh:

```latex
% Language
\usepackage[indonesian]{babel}

% Encoding
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

% Mathematics
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{mathtools}

% Graphics
\usepackage{graphicx}
\usepackage{float}

% Tables
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}

% Colors
\usepackage{xcolor}

% Code
\usepackage{listings}

% References
\usepackage{hyperref}
\usepackage{url}

% Chapter compilation
\usepackage{subfiles}

% Bibliography
\usepackage{natbib}
```

Jika sebuah package diperlukan oleh seluruh buku, package tersebut didefinisikan di sini.

---

# 6. `commands.tex`

Berisi custom command.

Contoh:

```latex
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}

\newcommand{\code}[1]{\texttt{#1}}

\newcommand{\important}[1]{
    \textbf{Penting:} #1
}
```

Tujuan utamanya adalah mencegah definisi command yang sama tersebar di berbagai bab.

---

# 7. `environments.tex`

Berisi environment khusus.

Contoh:

```latex
\newtheorem{definition}{Definisi}[chapter]
\newtheorem{theorem}{Teorema}[chapter]
\newtheorem{lemma}{Lemma}[chapter]
\newtheorem{example}{Contoh}[chapter]
```

Dapat ditambahkan environment untuk:

- definisi;
- teorema;
- lemma;
- contoh;
- catatan;
- latihan;
- tujuan pembelajaran;
- studi kasus.

---

# 8. `styles.tex`

Berisi konfigurasi tampilan buku.

Contoh:

```latex
\usepackage{titlesec}

\titleformat{\chapter}
    {\Huge\bfseries}
    {\thechapter}
    {1em}
    {}
```

Konfigurasi visual seperti:

- format chapter;
- format section;
- spacing;
- header/footer;
- warna;
- layout halaman;

diletakkan di sini.

---

# 9. `listings.tex`

Berisi konfigurasi source code.

Contoh:

```latex
\lstset{
    basicstyle=\ttfamily\small,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny,
    showstringspaces=false
}
```

Bahasa pemrograman dapat didefinisikan:

```latex
\lstdefinelanguage{MyLanguage}{
    ...
}
```

Dengan demikian seluruh buku menggunakan konfigurasi source code yang konsisten.

---

# 10. `main.tex`

Struktur final:

```latex
\documentclass[
    12pt,
    a4paper,
    oneside
]{book}

% =========================================================
% GLOBAL CONFIGURATION
% =========================================================

\input{preamble}
\input{metadata}

% =========================================================
% DOCUMENT
% =========================================================

\begin{document}

% =========================================================
% FRONT MATTER
% =========================================================

\frontmatter

\input{frontmatter/cover}
\input{frontmatter/copyright}
\input{frontmatter/preface}
\input{frontmatter/acknowledgements}
\input{frontmatter/learning-outcomes}

\tableofcontents
\listoffigures
\listoftables

% =========================================================
% MAIN MATTER
% =========================================================

\mainmatter

\include{chapters/01/chapter}
\include{chapters/02/chapter}
\include{chapters/03/chapter}
\include{chapters/04/chapter}

% Tambahkan bab berikutnya
% \include{chapters/05/chapter}
% \include{chapters/06/chapter}

% =========================================================
% APPENDICES
% =========================================================

\appendix

\input{appendices/appendix-a}
\input{appendices/appendix-b}

% =========================================================
% BACK MATTER
% =========================================================

\backmatter

\bibliographystyle{apalike}
\bibliography{references}

\end{document}
```

---

# 11. Arsitektur Bab

Setiap bab merupakan modul independen.

Contoh:

```text
chapters/
└── 01/
    ├── chapter.tex
    ├── section-01.tex
    ├── section-02.tex
    ├── section-03.tex
    ├── contoh.tex
    ├── praktikum.tex
    ├── latihan.tex
    ├── rangkuman.tex
    ├── evaluasi.tex
    └── figures/
```

Struktur logis:

```text
Chapter
│
├── Tujuan Pembelajaran
│
├── Section 1
│
├── Section 2
│
├── Section 3
│
├── Contoh
│
├── Praktikum
│
├── Latihan
│
├── Rangkuman
│
└── Evaluasi
```

---

# 12. `chapter.tex`

Contoh:

```latex
\documentclass[../../main.tex]{subfiles}

\begin{document}

\chapter{Konsep Dasar}

\section*{Tujuan Pembelajaran}

Setelah mempelajari bab ini, mahasiswa mampu:

\begin{enumerate}
    \item Menjelaskan konsep dasar.
    \item Mengidentifikasi komponen utama.
    \item Menerapkan konsep dalam contoh sederhana.
\end{enumerate}

\subfile{section-01}
\subfile{section-02}
\subfile{section-03}

\input{contoh}
\input{praktikum}
\input{latihan}
\input{rangkuman}
\input{evaluasi}

\end{document}
```

File ini mempunyai dua fungsi:

1. Dapat dikompilasi sebagai bab mandiri.
2. Dapat dipanggil oleh `main.tex`.

---

# 13. Mengapa `subfiles` Digunakan

Package:

```latex
\usepackage{subfiles}
```

memungkinkan struktur seperti:

```text
main.tex
   │
   ├── chapters/01/chapter.tex
   ├── chapters/02/chapter.tex
   └── chapters/03/chapter.tex
```

Ketika `main.tex` dikompilasi:

```text
main.tex
    ↓
seluruh bab
    ↓
satu PDF buku
```

Ketika:

```text
chapters/01/chapter.tex
```

dikompilasi:

```text
chapter.tex
    ↓
Bab 1
    ↓
PDF Bab 1
```

---

# 14. `subfile` vs `include` vs `input`

## `\include`

Digunakan untuk unit besar seperti bab.

```latex
\include{chapters/01/chapter}
```

Gunakan untuk:

```text
Chapter 1
Chapter 2
Chapter 3
...
```

---

## `\subfile`

Digunakan untuk file yang harus dapat dikompilasi sendiri.

```latex
\subfile{section-01}
```

File tersebut tetap dapat digunakan ketika parent document dikompilasi.

---

## `\input`

Digunakan untuk komponen kecil yang tidak perlu menjadi dokumen mandiri.

```latex
\input{latihan}
```

Contoh penggunaan:

```text
latihan.tex
rangkuman.tex
evaluasi.tex
```

---

# 15. Aturan Pemakaian

Gunakan aturan berikut:

```text
BAB
    ↓
\include

SECTION yang mandiri
    ↓
\subfile

Potongan kecil
    ↓
\input
```

Contoh:

```latex
\include{chapters/01/chapter}
```

kemudian:

```latex
\subfile{section-01}
\subfile{section-02}
```

kemudian:

```latex
\input{latihan}
\input{rangkuman}
\input{evaluasi}
```

---

# 16. Section

Contoh:

```latex
\section{Pengertian Dasar}

Materi pengantar.

\subsection{Definisi}

Penjelasan definisi.

\subsection{Karakteristik}

Penjelasan karakteristik.
```

Section tidak perlu memiliki:

```latex
\documentclass
```

karena merupakan bagian dari `chapter.tex`.

---

# 17. Gambar

Gambar yang hanya digunakan oleh satu bab ditempatkan di direktori bab:

```text
chapters/
└── 01/
    └── figures/
        ├── diagram-01.png
        ├── diagram-02.png
        └── architecture.png
```

Contoh:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[
        width=0.8\textwidth
    ]{figures/diagram-01.png}

    \caption{Diagram sistem}
    \label{fig:diagram-sistem}
\end{figure}
```

Referensi:

```latex
Seperti ditunjukkan pada
Gambar~\ref{fig:diagram-sistem}.
```

---

# 18. Gambar Global

Gambar yang digunakan oleh banyak bab dapat ditempatkan:

```text
assets/
└── images/
```

Contoh:

```text
assets/images/logo.png
assets/images/architecture.png
```

Gambar khusus bab:

```text
chapters/01/figures/
```

Gambar umum:

```text
assets/images/
```

---

# 19. Source Code

Source code tidak disimpan langsung dalam file `.tex` jika ukurannya besar.

Contoh:

```text
code/
├── cpp/
│   ├── hello.cpp
│   └── compiler.cpp
│
├── python/
│   ├── example.py
│   └── parser.py
│
├── pascal/
│   └── example.pas
│
└── matlab/
    └── example.m
```

Kemudian dimasukkan menggunakan:

```latex
\lstinputlisting[
    language=C++,
    caption={Program sederhana},
    label={lst:program-sederhana}
]{../../code/cpp/hello.cpp}
```

Keuntungan:

- source code dapat diuji secara terpisah;
- source code dapat digunakan kembali;
- perubahan source tidak mengharuskan penyalinan kode ke banyak file `.tex`.

---

# 20. Referensi

Seluruh bibliografi ditempatkan pada:

```text
references.bib
```

Contoh citation:

```latex
Menurut \cite{aho2006}, ...
```

atau:

```latex
Compiler merupakan ... \citep{aho2006}.
```

Jangan membuat file `.bib` berbeda untuk setiap bab kecuali memang terdapat kebutuhan khusus.

Tujuan utama:

```text
references.bib
       │
       ├── Chapter 1
       ├── Chapter 2
       ├── Chapter 3
       └── Chapter N
```

Satu sumber dapat digunakan oleh banyak bab.

---

# 21. Label

Gunakan sistem penamaan label yang konsisten.

## Chapter

```latex
\label{chap:konsep-dasar}
```

## Section

```latex
\label{sec:definisi}
```

## Figure

```latex
\label{fig:arsitektur}
```

## Table

```latex
\label{tab:perbandingan}
```

## Equation

```latex
\label{eq:persamaan-dasar}
```

## Listing

```latex
\label{lst:program}
```

Contoh:

```latex
\section{Definisi}
\label{sec:definisi}
```

Referensi:

```latex
Bagian~\ref{sec:definisi}
```

---

# 22. Aturan Penamaan File

Gunakan nama file sederhana dan konsisten.

Direkomendasikan:

```text
chapter.tex
section-01.tex
section-02.tex
section-03.tex
latihan.tex
rangkuman.tex
evaluasi.tex
```

Hindari:

```text
Section 1 Final.tex
Bab 1 revisi terbaru.tex
Materi Baru Final Fix.tex
```

Gunakan:

```text
section-01.tex
```

bukan:

```text
Section 01.tex
```

---

# 23. Nomor Bab

Nomor direktori menggunakan dua digit:

```text
01
02
03
...
09
10
11
...
16
```

Bukan:

```text
1
2
3
...
10
```

Dengan demikian urutan filesystem tetap benar:

```text
01
02
03
...
09
10
11
...
```

---

# 24. Front Matter

Direktori:

```text
frontmatter/
```

Contoh:

```text
frontmatter/
├── cover.tex
├── copyright.tex
├── preface.tex
├── acknowledgements.tex
└── learning-outcomes.tex
```

Contoh `preface.tex`:

```latex
\chapter*{Kata Pengantar}

Isi kata pengantar.

\cleardoublepage
```

---

# 25. Back Matter

Contoh:

```text
appendices/
├── appendix-a.tex
└── appendix-b.tex
```

Isi appendix:

```latex
\chapter{Referensi Tambahan}

Materi tambahan.
```

---

# 26. Kompilasi Seluruh Buku

Perintah:

```bash
pdflatex main.tex
```

Jika menggunakan bibliography:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Dalam praktik, lebih baik menggunakan `latexmk`:

```bash
latexmk -pdf main.tex
```

`latexmk` menangani kebutuhan kompilasi berulang secara otomatis.

---

# 27. Kompilasi Satu Bab

Misalnya Bab 1:

```bash
cd chapters/01
latexmk -pdf chapter.tex
```

Hasilnya adalah PDF Bab 1.

Bab lain:

```bash
cd chapters/02
latexmk -pdf chapter.tex
```

---

# 28. Script `build-all.bat`

Contoh:

```bat
@echo off

echo ========================================
echo Building complete book
echo ========================================

latexmk -pdf main.tex

echo.
echo Build completed.
pause
```

---

# 29. Script `build-chapter.bat`

Contoh:

```bat
@echo off

if "%~1"=="" (
    echo Usage:
    echo build-chapter.bat 01
    exit /b 1
)

echo ========================================
echo Building Chapter %~1
echo ========================================

cd chapters\%~1

latexmk -pdf chapter.tex

cd ..\..

echo.
echo Chapter build completed.
pause
```

Penggunaan:

```bat
scripts\build-chapter.bat 01
```

---

# 30. Script `clean.bat`

Contoh:

```bat
@echo off

echo Cleaning LaTeX auxiliary files...

latexmk -C main.tex

for /d %%D in (chapters\*) do (
    if exist "%%D\chapter.tex" (
        cd "%%D"
        latexmk -C chapter.tex
        cd ..\..
    )
)

echo Cleaning completed.
pause
```

---

# 31. Direktori `build`

Direktori:

```text
build/
```

digunakan untuk output build apabila konfigurasi build system diarahkan ke sana.

File sementara seperti:

```text
.aux
.log
.toc
.lof
.lot
.out
.fdb_latexmk
.fls
```

sebaiknya tidak menjadi bagian source utama.

Tambahkan ke `.gitignore` jika menggunakan Git.

---

# 32. `.gitignore`

Contoh:

```gitignore
# LaTeX auxiliary files
*.aux
*.log
*.toc
*.lof
*.lot
*.out
*.fls
*.fdb_latexmk
*.synctex.gz
*.bcf
*.run.xml
*.bbl
*.blg

# Build directory
build/

# Editor
.vscode/
.idea/
```

---

# 33. Workflow Pengembangan

Workflow yang direkomendasikan:

```text
1. Tentukan struktur buku
        ↓
2. Buat chapter
        ↓
3. Pecah chapter menjadi section
        ↓
4. Tulis materi
        ↓
5. Tambahkan contoh
        ↓
6. Tambahkan praktikum
        ↓
7. Tambahkan latihan
        ↓
8. Tambahkan rangkuman
        ↓
9. Tambahkan evaluasi
        ↓
10. Compile chapter
        ↓
11. Periksa hasil
        ↓
12. Compile seluruh buku
        ↓
13. Final review
```

---

# 34. Workflow Pengembangan Bab

Satu bab dapat dikembangkan secara independen.

Contoh:

```text
Chapter 05
    │
    ├── section-01.tex
    ├── section-02.tex
    ├── section-03.tex
    │
    ├── contoh.tex
    ├── praktikum.tex
    ├── latihan.tex
    ├── rangkuman.tex
    └── evaluasi.tex
```

Ketika mengembangkan Bab 5:

```text
Compile Chapter 5
       ↓
Periksa PDF
       ↓
Perbaiki
       ↓
Compile ulang
```

Tidak perlu mengompilasi seluruh buku pada setiap perubahan kecil.

---

# 35. Workflow dengan AI

Struktur ini cocok untuk AI coding/writing assistant karena konteks dapat dibatasi.

AI yang bekerja pada Bab 5 cukup diberikan konteks:

```text
chapters/05/
```

dan konfigurasi:

```text
preamble.tex
config/
metadata.tex
```

Tidak harus membaca seluruh source buku.

Workflow:

```text
AI
 │
 ├── Read architecture
 │
 ├── Read global configuration
 │
 ├── Read target chapter
 │
 ├── Modify target chapter
 │
 └── Compile target chapter
```

---

# 36. Aturan untuk AI

AI yang bekerja pada proyek harus mengikuti aturan:

### Rule 1 — Jangan mengubah struktur tanpa alasan

Jangan memindahkan file hanya karena alasan kosmetik.

### Rule 2 — Jangan menduplikasi konfigurasi

Jika command sudah tersedia:

```latex
\code{}
```

jangan membuat command baru yang memiliki fungsi sama.

### Rule 3 — Jangan memasukkan package ke chapter

Hindari:

```latex
\usepackage{...}
```

di `chapter.tex`.

Package harus berada di:

```text
config/packages.tex
```

### Rule 4 — Chapter harus dapat dikompilasi

Setelah perubahan:

```bash
latexmk -pdf chapter.tex
```

harus dapat dijalankan.

### Rule 5 — Jangan merusak chapter lain

Perubahan global harus diperiksa terhadap seluruh buku.

---

# 37. Pemisahan Konten dan Konfigurasi

Arsitektur harus mempertahankan pemisahan:

```text
TECHNICAL
│
├── main.tex
├── preamble.tex
├── config/
└── scripts/

CONTENT
│
├── frontmatter/
├── chapters/
└── appendices/

RESOURCES
│
├── assets/
├── code/
└── references.bib
```

Dengan demikian perubahan layout tidak harus menyentuh isi buku.

---

# 38. Arsitektur Dependency

Hubungan dependency:

```text
main.tex
   │
   ├── preamble.tex
   │       │
   │       └── config/
   │
   ├── metadata.tex
   │
   ├── frontmatter/
   │
   ├── chapters/
   │       │
   │       ├── 01/chapter.tex
   │       ├── 02/chapter.tex
   │       ├── 03/chapter.tex
   │       └── ...
   │
   ├── appendices/
   │
   └── references.bib
```

Sedangkan chapter:

```text
chapter.tex
   │
   ├── section-01.tex
   ├── section-02.tex
   ├── section-03.tex
   ├── contoh.tex
   ├── praktikum.tex
   ├── latihan.tex
   ├── rangkuman.tex
   └── evaluasi.tex
```

---

# 39. Prinsip Independensi Bab

Setiap bab harus mempunyai:

```text
chapter.tex
    ↓
self-contained compilation
```

Artinya:

```bash
latexmk -pdf chapters/05/chapter.tex
```

harus menghasilkan dokumen yang valid.

Namun `chapter.tex` tetap menggunakan:

```latex
\documentclass[../../main.tex]{subfiles}
```

sehingga konfigurasi tetap berasal dari master document.

---

# 40. Cross Reference Antar-Bab

Cross-reference antar-bab harus menggunakan `\label` dan `\ref`.

Contoh pada Bab 1:

```latex
\chapter{Pendahuluan}
\label{chap:pendahuluan}
```

Bab 5:

```latex
Pembahasan lanjutan dapat dilihat pada
Bab~\ref{chap:pendahuluan}.
```

Namun cross-reference antar-bab perlu diuji ketika bab dikompilasi sendiri.

Jika sebuah bab membutuhkan referensi terhadap bab lain, sistem harus menerima kemungkinan bahwa referensi tersebut tidak tersedia ketika chapter dikompilasi secara standalone.

---

# 41. Aturan Referensi Gambar

Jangan menulis:

```latex
Gambar 1
```

secara manual jika nomor gambar dapat berubah.

Gunakan:

```latex
Gambar~\ref{fig:arsitektur}
```

Demikian pula:

```latex
Tabel~\ref{tab:hasil}
```

dan:

```latex
Persamaan~\ref{eq:formula}
```

---

# 42. Aturan untuk Materi Pembelajaran

Untuk buku ajar, struktur setiap bab direkomendasikan:

```text
BAB
│
├── Judul
│
├── Tujuan Pembelajaran
│
├── Pendahuluan
│
├── Materi Utama
│   ├── Section 1
│   ├── Section 2
│   └── Section 3
│
├── Contoh
│
├── Praktikum
│
├── Latihan
│
├── Rangkuman
│
└── Evaluasi
```

Jika diperlukan dapat ditambahkan:

```text
├── Studi Kasus
├── Tugas
├── Proyek
└── Referensi Bab
```

---

# 43. Template Chapter

Template standar:

```latex
\documentclass[../../main.tex]{subfiles}

\begin{document}

\chapter{Judul Bab}

% =========================================================
% TUJUAN PEMBELAJARAN
% =========================================================

\section*{Tujuan Pembelajaran}

Setelah mempelajari bab ini, mahasiswa mampu:

\begin{enumerate}
    \item ...
    \item ...
    \item ...
\end{enumerate}

% =========================================================
% MATERI
% =========================================================

\subfile{section-01}
\subfile{section-02}
\subfile{section-03}

% =========================================================
% CONTOH
% =========================================================

\input{contoh}

% =========================================================
% PRAKTIKUM
% =========================================================

\input{praktikum}

% =========================================================
% LATIHAN
% =========================================================

\input{latihan}

% =========================================================
% RANGKUMAN
% =========================================================

\input{rangkuman}

% =========================================================
% EVALUASI
% =========================================================

\input{evaluasi}

\end{document}
```

---

# 44. Template Section

```latex
\section{Judul Section}
\label{sec:judul-section}

Paragraf pembuka.

\subsection{Subtopik}

Pembahasan.

\subsection{Subtopik Berikutnya}

Pembahasan.

\begin{example}
Contoh diberikan di sini.
\end{example}
```

---

# 45. Template Latihan

```latex
\section*{Latihan}

\begin{enumerate}

    \item Jelaskan ...

    \item Implementasikan ...

    \item Analisis ...

\end{enumerate}
```

---

# 46. Template Rangkuman

```latex
\section*{Rangkuman}

Pada bab ini telah dibahas:

\begin{itemize}
    \item ...
    \item ...
    \item ...
\end{itemize}
```

---

# 47. Template Evaluasi

```latex
\section*{Evaluasi}

\begin{enumerate}

    \item Soal evaluasi pertama.

    \item Soal evaluasi kedua.

    \item Soal evaluasi ketiga.

\end{enumerate}
```

---

# 48. Checklist Struktur

Sebelum proyek digunakan, pastikan:

- [ ] `main.tex` tersedia.
- [ ] `preamble.tex` tersedia.
- [ ] `metadata.tex` tersedia.
- [ ] `references.bib` tersedia.
- [ ] `config/` tersedia.
- [ ] `frontmatter/` tersedia.
- [ ] `chapters/` tersedia.
- [ ] `appendices/` tersedia.
- [ ] `assets/` tersedia.
- [ ] `code/` tersedia.
- [ ] `scripts/` tersedia.

---

# 49. Checklist Setiap Bab

Setiap bab harus memiliki:

- [ ] `chapter.tex`
- [ ] tujuan pembelajaran
- [ ] section utama
- [ ] contoh
- [ ] praktikum jika diperlukan
- [ ] latihan
- [ ] rangkuman
- [ ] evaluasi
- [ ] gambar yang diperlukan
- [ ] label/reference yang valid
- [ ] citation yang valid
- [ ] chapter dapat dikompilasi sendiri

---

# 50. Checklist Kompilasi

## Individual Chapter

```bash
latexmk -pdf chapters/01/chapter.tex
```

Pastikan:

- [ ] tidak ada error;
- [ ] tidak ada `undefined reference` yang tidak diharapkan;
- [ ] gambar muncul;
- [ ] tabel benar;
- [ ] source code benar;
- [ ] persamaan benar;
- [ ] citation benar.

## Full Book

```bash
latexmk -pdf main.tex
```

Pastikan:

- [ ] seluruh bab muncul;
- [ ] daftar isi benar;
- [ ] daftar gambar benar;
- [ ] daftar tabel benar;
- [ ] nomor bab benar;
- [ ] nomor section benar;
- [ ] cross-reference benar;
- [ ] bibliography benar;
- [ ] appendix benar.

---

# 51. Arsitektur Final

Struktur final secara konseptual:

```text
                         ┌────────────────────┐
                         │      main.tex      │
                         │   MASTER DOCUMENT  │
                         └─────────┬──────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
       FRONTMATTER             CHAPTERS              APPENDICES
             │                     │                     │
             │          ┌──────────┼──────────┐          │
             │          │          │          │          │
             │          ▼          ▼          ▼          │
             │        BAB 01     BAB 02     BAB N       │
             │          │          │          │          │
             │          ▼          ▼          ▼          │
             │       Sections   Sections   Sections      │
             │          │          │          │          │
             └──────────┴──────────┴──────────┴──────────┘
                                   │
                                   ▼
                              REFERENCES
                                   │
                                   ▼
                            references.bib
```

Konfigurasi berada di luar content:

```text
                 ┌──────────────────────┐
                 │      preamble.tex    │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
         packages        commands       styles
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     BOOK CONFIGURATION
```

---

# 52. Arsitektur Akhir yang Direkomendasikan

Struktur final:

```text
book/
│
├── main.tex
├── preamble.tex
├── metadata.tex
├── references.bib
│
├── config/
│   ├── packages.tex
│   ├── commands.tex
│   ├── environments.tex
│   ├── styles.tex
│   └── listings.tex
│
├── frontmatter/
│   ├── cover.tex
│   ├── copyright.tex
│   ├── preface.tex
│   ├── acknowledgements.tex
│   └── learning-outcomes.tex
│
├── chapters/
│   │
│   ├── 01/
│   │   ├── chapter.tex
│   │   ├── section-01.tex
│   │   ├── section-02.tex
│   │   ├── section-03.tex
│   │   ├── contoh.tex
│   │   ├── praktikum.tex
│   │   ├── latihan.tex
│   │   ├── rangkuman.tex
│   │   ├── evaluasi.tex
│   │   └── figures/
│   │
│   ├── 02/
│   │   └── ...
│   │
│   ├── 03/
│   │   └── ...
│   │
│   └── 16/
│       └── ...
│
├── appendices/
│   ├── appendix-a.tex
│   └── appendix-b.tex
│
├── assets/
│   ├── images/
│   ├── diagrams/
│   └── logos/
│
├── code/
│   ├── cpp/
│   ├── python/
│   ├── pascal/
│   └── matlab/
│
├── build/
│
└── scripts/
    ├── build-all.bat
    ├── build-chapter.bat
    └── clean.bat
```

Arsitektur ini memberikan dua target build:

```text
                    SOURCE BOOK
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
        main.tex                chapter.tex
              │                     │
              ▼                     ▼
       FULL BOOK PDF          SINGLE CHAPTER PDF
```

Dengan demikian, **`main.tex` menjadi master document**, sedangkan **setiap `chapters/XX/chapter.tex` menjadi unit kompilasi mandiri**. `config/` menangani konfigurasi global, `chapters/` menangani konten, `assets/` menangani aset visual, `code/` menangani source code, dan `references.bib` menjadi sumber bibliografi bersama seluruh buku.
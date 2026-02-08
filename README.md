# Pemrograman Game

**Program Studi S1 Informatika**

## Deskripsi Mata Kuliah

Mata kuliah **Pemrograman Game** membekali mahasiswa dengan pengetahuan dan keterampilan praktis dalam pengembangan game menggunakan **Unity Engine** dan bahasa pemrograman **C#**. Mata kuliah ini mengadopsi pendekatan *Outcome-Based Education (OBE)* dengan fokus pada pembelajaran berbasis proyek (*project-based learning*).

### 🎯 **Fokus Pembelajaran**
- Konsep dasar game development dan desain
- Workflow pengembangan game di Unity
- Pemrograman C# untuk game logic
- Fisika, animasi, UI/UX, dan audio dalam game
- Artificial Intelligence (AI) sederhana untuk NPC
- Proses build dan deployment ke berbagai platform

## 🏗️ **Struktur Proyek**

```
kuliah_pemrograman_game/
├── 📖 book/                     # Buku ajar utama
│   ├── main.tex                 # Dokumen utama
│   ├── preamble.tex             # Konfigurasi LaTeX
│   ├── frontmatter.tex          # Halaman awal
│   ├── backmatter.tex          # Halaman akhir
│   ├── references.bib          # Bibliografi
│   ├── chapters/              # 16 bab OBE
│   │   ├── bab-01/          # Bab 1: Pendahuluan
│   │   ├── bab-02/          # Bab 2: Landasan Teori
│   │   ├── ...              # Bab 3-15
│   │   └── bab-16/          # Bab 16: Publishing
│   │       ├── bab-XX.tex   # File utama bab
│   │       └── section-XX-Y.tex # 5 section per bab
│   └── archive/             # Bab legacy (tidak digunakan)
├── 🔧 *.bat                 # Batch files otomasi
├── 💻 code/                 # Script pendukung
├── 📄 output/               # Hasil kompilasi PDF
└── 📋 README.md             # Dokumentasi ini
```

## 🚀 **Quick Start**

### **Prerequisites**
- **MiKTeX** atau **TeX Live** (untuk kompilasi LaTeX)
- **Unity Editor** (untuk praktikum)
- **Visual Studio Code** (recommended editor)

### **Kompilasi Buku Ajar**

#### **Metode 1: Interactive (Recommended)**
```batch
compile_quick.bat
```
Pilih opsi:
1. Complete Book → `output/main.pdf`
2. All Chapters → `output/bab-01.pdf` hingga `bab-16.pdf`
3. Single Chapter → Input nomor bab

#### **Metode 2: Command Line**
```batch
# Kompilasi buku lengkap
compile_book.bat

# Kompilasi semua bab
compile_chapters.bat

# Kompilasi bab spesifik
compile_chapter.bat 14
```

### **Membersihkan File Kompilasi**

```batch
# Clean interaktif (recommended)
clean_quick.bat

# Clean total semua file
clean_all.bat

# Clean comprehensive dengan reporting
clean_project.bat
```

## 📖 **Buku Ajar OBE**

### **Struktur Setiap Bab**
Setiap bab mengikuti format OBE yang konsisten:

```
bab-XX/
├── bab-XX.tex              # File utama bab
├── section-XX-1.tex        # Materi Pokok 1
├── section-XX-2.tex        # Materi Pokok 2
├── section-XX-3.tex        # Materi Pokok 3
├── section-XX-4.tex        # Materi Pokok 4
└── section-XX-5.tex        # Materi Pokok 5
```

### **Komponen OBE per Bab**
- **Sub-CPMK** - Capaian Pembelajaran Khusus
- **Materi Pokok** - Konten teori dan praktik
- **Aktivitas Pembelajaran** - Hands-on exercises
- **Latihan OBE** - Soal latihan terstruktur
- **Asesmen** - Rubrik dan evaluasi
- **Checklist Kompetensi** - Self-assessment
- **Rangkuman** - Review materi

### **Daftar Bab Lengkap**

| Bab | Topik | Fokus Utama |
|------|-------|-------------|
| 1 | Pendahuluan dan Orientasi | OBE Framework |
| 2 | Landasan Teori | Konsep Dasar Game |
| 3 | Konsep Dasar Game Development | Game Design |
| 4 | Pengenalan Unity Engine | Unity Basics |
| 5 | Dasar Pemrograman C# | C# Fundamentals |
| 6 | GameObject, Component, Prefab | Unity Objects |
| 7 | Input System & Player Controller | Game Controls |
| 8 | Physics, Collision, Rigidbody | Game Physics |
| 9 | Animation & Animator | Game Animation |
| 10 | UI System & Interface Design | User Interface |
| 11 | Particles & Visual Effects | Visual Effects |
| 12 | Shaders & Materials | Graphics Programming |
| 13 | Networking & Multiplayer | Multiplayer Games |
| 14 | Post-Processing & Visual Effects | Advanced Graphics |
| 15 | Game Optimization & Performance | Performance Tuning |
| 16 | Game Publishing & Deployment | Release Management |

## 🛠️ **Tools & Scripts**

### **Batch Files**
- `compile_quick.bat` - Menu kompilasi interaktif
- `compile_book.bat` - Kompilasi buku lengkap
- `compile_chapters.bat` - Kompilasi semua bab
- `compile_chapter.bat` - Kompilasi bab spesifik
- `clean_quick.bat` - Pembersihan interaktif
- `clean_project.bat` - Pembersihan komprehensif
- `clean_all.bat` - Pembersihan total

### **Python Scripts**
- `code/download_image.py` - Download gambar untuk dokumentasi
- `code/gen_table.py` - Generate tabel otomatis

## 📋 **Capaian Pembelajaran**

Setelah menyelesaian mata kuliah ini, mahasiswa diharapkan mampu:

### **CPL (Capaian Pembelajaran Lulusan)**
- **CPL-01**: Mampu menerapkan pengetahuan matematika, sains, dan rekayasa
- **CPL-02**: Mampu merancang dan menguji sistem komputer
- **CPL-03**: Mampu mengembangkan perangkat lunak berbasis teknologi terkini
- **CPL-04**: Mampu beradaptasi dengan perkembangan teknologi

### **CPMK (Capaian Pembelajaran Mata Kuliah)**
- **CPMK-1**: Memahami konsep dasar pengembangan game
- **CPMK-2**: Menerapkan workflow pengembangan di Unity
- **CPMK-3**: Mengimplementasikan logika game dengan C#
- **CPMK-4**: Mengintegrasikan sistem fisika dan animasi
- **CPMK-5**: Membangun UI/UX yang efektif
- **CPMK-6**: Mengoptimalkan performa game
- **CPMK-7**: Mempublish game ke platform target

## 📊 **Evaluasi & Asesmen**

### **Komponen Penilaian**
- **Tugas Praktikum**: 25%
- **Kuis**: 10%
- **UTS**: 20%
- **Proyek Akhir**: 30%
- **UAS**: 15%

### **Rubrik Asesmen**
- **Kriteria Penilaian**:
  - Fungsionalitas (40%)
  - Kualitas Code (25%)
  - Design & UX (20%)
  - Dokumentasi (15%)

## 🎮 **Praktikum & Proyek**

### **Format Praktikum**
- **Hands-on Coding** - Implementasi langsung di Unity
- **Mini Projects** - Proyek kecil per topik
- **Case Studies** - Analisis game existing
- **Peer Review** - Review dan feedback sesama mahasiswa

### **Proyek Akhir**
- **Game Development** - Buat game lengkap dari konsep hingga publish
- **Portfolio** - Dokumentasi proses dan hasil
- **Presentation** - Presentasi dan demo

## 📝 **Rencana Pembelajaran Semester (RPS)**

| Pertemuan | Topik Materi | Output |
| :--- | :--- | :--- |
| 1 | Konsep Dasar Game Development & Pengenalan Unity | Project Setup |
| 2 | Unity Editor Interface & Project Structure | Scene Creation |
| 3 | Dasar Pemrograman C# untuk Unity | Basic Scripts |
| 4 | GameObject, Component, Transform, & Prefab | Object Manipulation |
| 5 | Input System & Player Controller | Player Movement |
| 6 | Physics System, Collision, & Rigidbody | Physics Simulation |
| 7 | Animasi Karakter (Animator Controller) | Character Animation |
| **8** | **UTS (Ujian Tengah Semester)** | **Midterm Exam** |
| 9 | UI/UX Game (Canvas, HUD, Menu) | User Interface |
| 10 | Integrasi Audio (SFX & BGM) | Audio System |
| 11 | Level Design & Game Mechanics | Level Creation |
| 12 | AI Sederhana (NavMesh & State Machine) | AI Behavior |
| 13 | Optimization & Profiling | Performance Tuning |
| 14 | Build & Deployment (PC, Mobile, Web) | Game Publishing |
| 15 | Finalisasi Proyek Game Akhir | Project Finalization |
| **16** | **UAS (Ujian Akhir Semester) - Presentasi Proyek** | **Final Presentation** |

## 💻 **Persyaratan Sistem**

### **Perangkat Lunak**
- **Unity Hub** & **Unity Editor** (LTS Version)
- **Visual Studio** atau **Visual Studio Code**
- **Git**
- **MiKTeX** atau **TeX Live** (untuk kompilasi dokumen)

### **Perangkat Keras (Minimal)**
- Processor: Intel Core i5 / AMD equivalent
- RAM: 8 GB (16 GB recommended)
- Graphics: DirectX 11 compatible
- Storage: 20 GB free space

## 🔗 **Referensi & Sumber**

### **Buku Referensi**
1. Unity Technologies. *Unity User Manual* & *Scripting API*.
2. Schell, J. (2019). *The Art of Game Design*.
3. Nystrom, R. (2014). *Game Programming Patterns*.
4. Gregory, J. (2018). *Game Engine Architecture*.

### **Online Resources**
- [Unity Learn](https://learn.unity.com/)
- [Unity Documentation](https://docs.unity3d.com/)
- [C# Programming Guide](https://docs.microsoft.com/en-us/dotnet/csharp/)

## 📝 **Catatan Penting**

### **Untuk Dosen**
- Gunakan `compile_quick.bat` untuk kompilasi cepat
- Archive chapters tersedia di `book/chapters/archive/`
- Template OBE sudah terstruktur di setiap bab

### **Untuk Mahasiswa**
- Praktikkan setiap contoh code di Unity
- Gunakan checklist kompetensi untuk self-assessment
- Ikuti urutan bab untuk pembelajaran optimal

### **Untuk Developer**
- Proyek menggunakan LaTeX dengan `subfiles` package
- Setiap bab dapat dikompilasi independen
- Batch files otomatisasi untuk workflow efisien

## 🤝 **Kontribusi**

### **Guidelines**
- Ikuti struktur OBE yang sudah ada
- Gunakan format LaTeX yang konsisten
- Test kompilasi sebelum commit
- Update dokumentasi jika ada perubahan

### **Version Control**
```bash
# Sebelum kompilasi
clean_quick.bat

# Kompilasi dan test
compile_quick.bat

# Commit changes
git add .
git commit -m "Update bab-X content"
```

## 📞 **Support & Kontak**

### **Technical Support**
- **LaTeX Issues**: Check `.log` files untuk error details
- **Unity Issues**: Consult Unity documentation
- **Code Issues**: Debug dengan Unity Console

### **Academic Support**
- **Konsultasi**: Jadwal dosen tersedia di SIAKAD
- **Forum**: Diskusi di platform pembelajaran
- **Tutoring**: Session tutoring terjadwal

## 📄 **Lisensi**

Proyek ini dilisensikan under [MIT License](LICENSE).

---

**Last Updated**: 2026

**Version**: 1.0.0

**Status**: Production Ready

---

*🎮 Selamat belajar dan happy coding! 🚀*

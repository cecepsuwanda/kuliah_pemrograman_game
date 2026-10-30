# Gudang Artefak -- GDD Satu Halaman

**Kelompok:** Tiga / **Versi:** 1.0 / **Tanggal:** minggu 15

## Identitas

- **Judul:** Gudang Artefak
- **Jenis:** platformer 2D bertampilan samping
- **Platform:** Windows, build Unity LTS
- **Durasi satu sesi:** 5-10 menit
- **Jumlah pemain:** satu orang

## Inti permainan

Pemain masuk ke gudang tua, melompati rak, dan mengumpulkan tiga artefak.
Setelah ketiganya terkumpul, pintu keluar terbuka. Pemain memiliki tiga nyawa;
nyawa berkurang ketika menyentuh bahaya, dan permainan berakhir ketika nyawa
habis.

## Kontrol

| Tombol | Tindakan |
|---|---|
| Panah kiri/kanan atau A/D | berjalan mendatar |
| Space | melompat, hanya ketika menyentuh tanah |
| Esc | keluar dari permainan |

## Aturan menang dan kalah

- **Menang:** pemain menyentuh pintu setelah ketiga artefak diambil.
- **Kalah:** nyawa mencapai nol.
- Pintu menolak pemain selama artefak belum lengkap dan menampilkan pesan
  pada Console.

## Isi level

- Satu level, yaitu Level Rak, dengan lantai dan tiga rak bertingkat.
- Tiga artefak pada ketinggian berbeda.
- Satu pintu keluar di ujung kanan level.
- Musik latar berulang dan tiga efek suara: lompat, mengambil artefak, kalah.

## Umpan balik

| Peristiwa | Terlihat | Terdengar |
|---|---|---|
| Melompat | animasi lompat | efek lompat |
| Mengambil artefak | skor bertambah, artefak lenyap | efek ambil |
| Nyawa berkurang | teks dan ikon nyawa berubah | efek kalah pada nyawa terakhir |
| Mencapai pintu | pesan Console | musik berhenti |

## Di luar lingkup

- Musuh yang mengejar dan pencarian jalur.
- Penyimpanan skor antarsesi.
- Level kedua.
- Pengaturan volume pada menu.

## Kriteria selesai

Build dinyatakan selesai apabila seluruh butir pada
`checklist-fungsional.md` lulus, tidak ada bug berat yang terbuka, dan satu
kali penyelesaian penuh berlangsung antara lima dan sepuluh menit.

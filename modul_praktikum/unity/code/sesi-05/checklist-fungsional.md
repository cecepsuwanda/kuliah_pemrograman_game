# Checklist Fungsional — Gudang Artefak

Build: `GudangArtefak-v1.0` / Tanggal: minggu 15
Diisi setiap putaran: L = lulus, T = tidak lulus.

| No | Kelompok | Butir pemeriksaan | P1 | P2 |
|---|---|---|---|---|
| 1 | Mekanik | Pemain berjalan ke kiri dan kanan dengan panah atau A/D | L | L |
| 2 | Mekanik | Pemain melompat hanya ketika menyentuh tanah | L | L |
| 3 | Mekanik | Pemain tidak dapat melompat berkali-kali di udara | T | L |
| 4 | Mekanik | Pemain dapat naik dari lantai ke rak pertama dan kedua | L | L |
| 5 | Mekanik | Artefak lenyap dan skor bertambah ketika disentuh | L | L |
| 6 | Mekanik | Pintu menolak pemain selama artefak belum lengkap | L | L |
| 7 | Mekanik | Pintu menerima pemain setelah ketiga artefak diambil | L | L |
| 8 | Integrasi | Animasi diam, berlari, dan melompat berganti sesuai keadaan | L | T |
| 9 | Integrasi | Bunyi lompat terdengar seketika ketika tombol ditekan | L | L |
| 10 | Integrasi | Bunyi ambil terdengar pada setiap artefak | T | L |
| 11 | Integrasi | Musik berhenti dan bunyi kalah terdengar ketika nyawa habis | L | L |
| 12 | Integrasi | Teks skor dan nyawa sesuai dengan keadaan permainan | L | L |
| 13 | Keseluruhan | Level dapat diselesaikan dari awal sampai pintu tanpa berhenti | L | L |
| 14 | Keseluruhan | Tidak ada tempat yang membuat pemain tidak dapat melanjutkan | T | L |
| 15 | Keseluruhan | Satu kali penyelesaian berlangsung 5–10 menit | L | L |
| 16 | Mekanik | Pemain tidak menembus lantai atau rak saat melompat | L | L |
| 17 | Integrasi | Musik latar berulang tanpa jeda yang terdengar | L | L |
| 18 | Integrasi | Partikel muncul ketika artefak diambil (bila dipakai) | L | L |
| 19 | Keseluruhan | Build berjalan pada komputer lain tanpa Unity | L | L |
| 20 | Keseluruhan | Console bersih dari pesan merah selama satu sesi | L | L |

Jumlah butir yang lulus: P1 = 17 dari 20; P2 = 19 dari 20.

Butir yang belum lulus dan alasannya:

- Butir 3 (P1): pemain masih dapat melompat dua kali pada tepi rak.
- Butir 8 (P2): animasi diam bertahan sesaat setelah pemain mendarat.
- Butir 10 (P1): artefak ketiga tidak berbunyi.
- Butir 14 (P1): sudut kanan bawah rak kanan membentuk lubang dangkal.

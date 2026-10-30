# Log Bug — Gudang Artefak

Build: `GudangArtefak-v1.0` / Diperbarui: minggu 15
Berat: Berat / Sedang / Ringan. Status: Terbuka / Selesai / Ditunda.

| No | Jenis | Urutan yang menyebabkannya dan hasil yang salah | Berat | Status |
|---|---|---|---|---|
| 1 | Integrasi | Ambil artefak 1 dan 2, lalu artefak 3. Artefak 3 lenyap dan skor bertambah, tetapi bunyi ambil tidak terdengar. | Sedang | Selesai |
| 2 | Mekanik | Berjalan ke tepi rak, melompat, lalu tekan Space sekali lagi sebelum mendarat. Pemain melompat lagi di udara. | Sedang | Selesai |
| 3 | Integrasi | Biarkan musik berjalan, lalu habiskan nyawa. Musik berhenti, tetapi bunyi kalah tidak terdengar karena klip `kalah` belum diisi pada ManajerBunyi. | Ringan | Selesai |
| 4 | Tampilan | Mendarat setelah lompatan panjang, lalu segera berjalan. Animasi diam bertahan sekitar satu detik sebelum animasi berlari muncul. | Ringan | Terbuka |
| 5 | Keseluruhan | Berjalan ke sudut kanan bawah rak kanan dan melompat ke arah dinding. Pemain jatuh ke celah dangkal dan harus melompat tiga kali untuk keluar. | Berat | Selesai |
| 6 | Tampilan | Mainkan pada jendela 4:3. Teks nyawa bertumpuk dengan ikon nyawa ketiga. | Ringan | Ditunda |

## Catatan perbaikan

- **No. 1:** medan `Pemicu Bunyi` pada artefak ketiga kosong. Diisi, lalu
  diuji ulang pada putaran 2; butir 10 lulus.
- **No. 2:** lingkaran pemeriksaan tanah masih menyentuh tepi rak ketika pemain
  sudah di udara. `Ground Radius` diperkecil dari 0,15 menjadi 0,12 dan
  `TitikTanah` diturunkan 0,05 satuan. Butir 3 lulus pada putaran 2.
- **No. 5:** collider rak kanan diperlebar 0,2 satuan. Butir 14 lulus pada
  putaran 2.
- **No. 4 dan 6:** dicatat sebagai kekurangan yang diketahui; tidak
  memengaruhi penyelesaian permainan.

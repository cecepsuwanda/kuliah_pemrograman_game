#!/usr/bin/env python3
"""Pemeriksa konsistensi proyek Buku Ajar Pengantar Pemrograman Game.

Pemeriksaan yang dilakukan:
  1. Kelengkapan berkas setiap bab.
  2. Cakupan CPL, CPMK, dan seluruh Sub-CPMK.
  3. Kesesuaian setiap \\cite dengan \\bibitem pada references.tex.
  4. Keberadaan berkas gambar, diagram TikZ, dan kode yang dipanggil.
  5. Kesesuaian setiap \\ref dengan \\label, serta label ganda.
  6. Kesesuaian daftar \\subfile aktif pada main.tex dengan direktori bab.

Jalankan dari direktori mana pun:

    python -I scripts/periksa_buku.py

Kode keluar 0 bila tidak ada temuan, 1 bila ada temuan.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "chapters"

# Bab yang tergolong bab inti (satu bab = satu materi = satu Sub-CPMK).
# Bab lain (I, II, XVII) memakai susunan yang lebih longgar.
BAB_INTI = {f"{n:02d}" for n in range(3, 17)}

BERKAS_INTI = (
    "chapter.tex",
    "sub-cpmk.tex",
    "tujuan.tex",
    "contoh.tex",
    "praktikum.tex",
    "latihan.tex",
    "rangkuman.tex",
    "checklist.tex",
    "evaluasi.tex",
)
BERKAS_DASAR = ("chapter.tex", "latihan.tex", "rangkuman.tex", "evaluasi.tex")

SUBCPMK_DIHARAPKAN = [
    "1.1", "1.2", "1.3", "1.4",
    "2.1", "2.2", "2.3", "2.4",
    "3.1", "3.2",
    "4.1", "4.2", "4.3",
]
CPL_DIHARAPKAN = ["03", "04"]
CPMK_DIHARAPKAN = ["1", "2", "3", "4"]

RE_KOMENTAR = re.compile(r"(?:(?<=\s)|^)%.*")
# Catatan: tanda % di dalam URL (misalnya %20) tidak dianggap komentar,
# sehingga tautan panjang pada references.tex tidak terpotong.
RE_LABEL = re.compile(r"\\label\{([^}]*)\}")
# Label juga dapat lahir dari pemanggil kode: argumen ketiga \kodepython dan
# \kodecsharp, serta pilihan label= pada \lstinputlisting.
RE_LABEL_KODE = re.compile(r"\\kode(?:python|csharp)\{[^}]*\}\{[^}]*\}\{([^}]*)\}")
RE_LABEL_LISTING = re.compile(r"\\lstinputlisting\[[^\]]*label=\{([^}]*)\}")
RE_REF = re.compile(r"\\(?:ref|eqref|autoref|pageref)\{([^}]*)\}")
RE_REFBAB = re.compile(r"\\refbab\{([^}]*)\}")
RE_CITE = re.compile(r"\\cite\{([^}]*)\}")
RE_BIBITEM = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}")
RE_INCLUDEGRAPHICS = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}")
RE_ASSETFILE = re.compile(r"\\assetfile\{([^}]*)\}")
RE_CODEFILE = re.compile(r"\\codefile\{([^}]*)\}")
RE_KODEPY = re.compile(r"\\kode(?:python|csharp)\{([^}]*)\}")
RE_LISTING = re.compile(r"\\lstinputlisting(?:\[[^\]]*\])?\{([^}]*)\}")
RE_INPUT = re.compile(r"\\input\{([^}]*)\}")
RE_SUBFILE_AKTIF = re.compile(r"^\s*\\subfile\{chapters/(\d\d)/chapter\}")
RE_SUBCPMK_DEF = re.compile(r"\\SUBCPMK\{([^}]*)\}")
RE_SUBCPMK_ISI = re.compile(r"\\SUBCPMK\{([^}]*)\}|\\subcpmk\{([^}]*)\}")
RE_CPL = re.compile(r"\\CPL\{([^}]*)\}")
RE_CPMK = re.compile(r"\\CPMK\{([^}]*)\}")

# Isi \code{...} ditampilkan apa adanya melalui \detokenize, sehingga tanda
# garis bawah dan tanda hubung ganda TIDAK boleh di-escape dengan gaya LaTeX.
TERLARANG_DI_CODE = ("\\_", "-{}-", "\\textbackslash", "\\{", "\\}",
                     "\\#", "\\%", "\\&")

# Lingkungan kodekeluaran bersifat verbatim: perintah LaTeX di dalamnya
# tercetak apa adanya, bukan dijalankan.
TERLARANG_DI_KELUARAN = (
    "\\code{", "\\istilah{", "\\textbackslash", "\\textbf{", "\\textit{",
    "\\mbox{", "\\ref{", "\\cite{",
)
RE_KELUARAN = re.compile(
    r"\\begin\{kodekeluaran\}(.*?)\\end\{kodekeluaran\}", re.DOTALL
)

# Nama lingkungan, untuk memeriksa kecocokan \begin dan \end.
RE_BEGIN = re.compile(r"\\begin\{([^}]*)\}")
RE_END = re.compile(r"\\end\{([^}]*)\}")
RE_TUTUP_HTML = re.compile(r"</([A-Za-z][A-Za-z0-9]*box)>")
RE_KOSONG = re.compile(r"\\(CPL|CPMK|SUBCPMK|ind|ref|label|cite)\{\}")

# \code harus selalu diikuti tanda '{'. Bentuk seperti \codNAMA} menandakan
# berkas rusak, misalnya akibat penyuntingan otomatis yang salah posisi.
RE_CODE_RUSAK = re.compile(r"\\cod(?!e\{|efile\{)")


class Temuan:
    """Kumpulan temuan pemeriksaan."""

    def __init__(self) -> None:
        self.galat: list[str] = []
        self.catatan: list[str] = []

    def salah(self, pesan: str) -> None:
        self.galat.append(pesan)

    def info(self, pesan: str) -> None:
        self.catatan.append(pesan)


def baca_tex(path: Path) -> str:
    """Membaca berkas .tex tanpa komentar."""
    teks = path.read_text(encoding="utf-8", errors="replace")
    return "\n".join(RE_KOMENTAR.sub("", baris) for baris in teks.splitlines())


def kumpulkan_tex() -> dict[Path, str]:
    """Mengumpulkan seluruh berkas .tex proyek beserta isinya tanpa komentar."""
    berkas: dict[Path, str] = {}
    for pola in ("main.tex", "*.tex", "frontmatter/*.tex", "appendices/*.tex",
                 "chapters/*/*.tex"):
        for path in ROOT.glob(pola):
            if path.is_file():
                berkas[path.resolve()] = baca_tex(path)
    return berkas


def rel(path: Path) -> str:
    """Nama berkas relatif terhadap akar proyek."""
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def periksa_kelengkapan(temuan: Temuan) -> list[str]:
    """Memeriksa kelengkapan berkas setiap bab. Mengembalikan daftar bab selesai."""
    bab_selesai: list[str] = []
    for nomor in sorted(p.name for p in CHAPTERS_DIR.iterdir() if p.is_dir()):
        direktori = CHAPTERS_DIR / nomor
        if not (direktori / "chapter.tex").exists():
            temuan.info(f"Bab {nomor}: belum dibuat.")
            continue

        bab_selesai.append(nomor)
        wajib = BERKAS_INTI if nomor in BAB_INTI else BERKAS_DASAR
        for nama in wajib:
            path = direktori / nama
            if not path.exists():
                temuan.salah(f"Bab {nomor}: berkas {nama} belum ada.")
            elif not baca_tex(path).strip():
                temuan.salah(f"Bab {nomor}: berkas {nama} kosong.")

        if nomor in BAB_INTI:
            section = sorted(direktori.glob("section-*.tex"))
            if not section:
                temuan.salah(f"Bab {nomor}: belum ada berkas section-*.tex.")
            for path in section:
                if not baca_tex(path).strip():
                    temuan.salah(f"Bab {nomor}: berkas {path.name} kosong.")
    return bab_selesai


def periksa_capaian(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa cakupan CPL, CPMK, dan Sub-CPMK."""
    teks_chapters = "\n".join(
        isi for path, isi in berkas.items() if "chapters" in path.parts
    )

    ditemukan_cpl = set(RE_CPL.findall(teks_chapters))
    for kode in CPL_DIHARAPKAN:
        if kode not in ditemukan_cpl:
            temuan.salah(f"Capaian: CPL{kode} belum dirujuk pada berkas bab mana pun.")

    ditemukan_cpmk = set(RE_CPMK.findall(teks_chapters))
    for kode in CPMK_DIHARAPKAN:
        if kode not in ditemukan_cpmk:
            temuan.salah(f"Capaian: CPMK{kode} belum dirujuk pada berkas bab mana pun.")

    ditemukan_sub = set()
    for a, b in RE_SUBCPMK_ISI.findall(teks_chapters):
        ditemukan_sub.add(a or b)
    for kode in SUBCPMK_DIHARAPKAN:
        if kode not in ditemukan_sub:
            temuan.salah(f"Capaian: Sub-CPMK {kode} belum ada pada berkas bab mana pun.")
    temuan.info(
        f"Capaian: {len(ditemukan_cpl)}/{len(CPL_DIHARAPKAN)} CPL, "
        f"{len(ditemukan_cpmk)}/{len(CPMK_DIHARAPKAN)} CPMK, "
        f"{len(ditemukan_sub & set(SUBCPMK_DIHARAPKAN))}/{len(SUBCPMK_DIHARAPKAN)} Sub-CPMK."
    )


def periksa_sitasi(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa kesesuaian \\cite dengan \\bibitem."""
    references = ROOT / "references.tex"
    if not references.exists():
        temuan.salah("references.tex tidak ditemukan.")
        return

    kunci_bib = set(RE_BIBITEM.findall(baca_tex(references)))
    if not kunci_bib:
        temuan.salah("references.tex tidak memuat satu pun \\bibitem.")

    kunci_dipakai: dict[str, Path] = {}
    for path, isi in berkas.items():
        if path.name == "references.tex":
            continue
        for isi_cite in RE_CITE.findall(isi):
            for kunci in isi_cite.split(","):
                kunci = kunci.strip()
                if kunci:
                    kunci_dipakai.setdefault(kunci, path)

    for kunci, path in sorted(kunci_dipakai.items()):
        if kunci not in kunci_bib:
            temuan.salah(f"Sitasi: \\cite{{{kunci}}} pada {rel(path)} tidak ada di references.tex.")

    belum_dipakai = sorted(kunci_bib - set(kunci_dipakai))
    if belum_dipakai:
        temuan.info(
            f"Sitasi: {len(kunci_bib) - len(belum_dipakai)}/{len(kunci_bib)} entri "
            f"pustaka sudah dipakai pada bab."
        )


def cari_berkas(kandidat: list[Path]) -> Path | None:
    """Mengembalikan kandidat pertama yang benar-benar ada."""
    for path in kandidat:
        if path.exists():
            return path
    return None


def periksa_rujukan_berkas(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa keberadaan gambar, diagram TikZ, dan berkas kode yang dipanggil."""
    for path, isi in sorted(berkas.items()):
        if "chapters" not in path.parts:
            continue
        direktori = path.parent

        for nama in RE_INCLUDEGRAPHICS.findall(isi):
            if "\\assetfile" in nama:
                dalam = RE_ASSETFILE.search(nama)
                if dalam:
                    target = ROOT / "assets" / dalam.group(1)
                    if not target.exists():
                        temuan.salah(f"Gambar: {rel(path)} memanggil {rel(target)} yang tidak ada.")
                continue
            if cari_berkas([direktori / nama, ROOT / nama, ROOT / "assets" / nama]) is None:
                temuan.salah(f"Gambar: {rel(path)} memanggil '{nama}' yang tidak ada.")

        for nama in RE_ASSETFILE.findall(isi):
            target = ROOT / "assets" / nama
            if not target.exists():
                temuan.salah(f"Gambar: {rel(path)} memanggil {rel(target)} yang tidak ada.")

        for nama in RE_INPUT.findall(isi):
            if not nama.endswith(".tikz"):
                continue
            if cari_berkas([direktori / nama, ROOT / nama]) is None:
                temuan.salah(f"Diagram: {rel(path)} memanggil '{nama}' yang tidak ada.")

        for nama in RE_CODEFILE.findall(isi) + RE_KODEPY.findall(isi):
            target = ROOT / "code" / nama
            if not target.exists():
                temuan.salah(f"Kode: {rel(path)} memanggil {rel(target)} yang tidak ada.")

        for nama in RE_LISTING.findall(isi):
            if "\\codefile" in nama:
                continue
            target = ROOT / "code" / nama
            if not target.exists():
                temuan.salah(f"Kode: {rel(path)} memanggil {rel(target)} yang tidak ada.")


def periksa_label(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa label ganda dan \\ref tanpa label."""
    lokasi_label: dict[str, Path] = {}
    for path, isi in berkas.items():
        semua = (RE_LABEL.findall(isi)
                 + RE_LABEL_KODE.findall(isi)
                 + RE_LABEL_LISTING.findall(isi))
        for label in semua:
            if label in lokasi_label:
                temuan.salah(
                    f"Label: '{label}' didefinisikan lebih dari sekali "
                    f"({rel(lokasi_label[label])} dan {rel(path)})."
                )
            else:
                lokasi_label[label] = path

    for path, isi in berkas.items():
        if "chapters" not in path.parts:
            continue
        for target in RE_REF.findall(isi) + RE_REFBAB.findall(isi):
            if target and target not in lokasi_label:
                temuan.salah(f"Rujukan: {rel(path)} memakai \\ref{{{target}}} tanpa \\label.")


def periksa_main(temuan: Temuan, bab_selesai: list[str]) -> None:
    """Memeriksa daftar \\subfile aktif pada main.tex."""
    main = ROOT / "main.tex"
    if not main.exists():
        temuan.salah("main.tex tidak ditemukan.")
        return

    aktif = set()
    for baris in main.read_text(encoding="utf-8", errors="replace").splitlines():
        if baris.lstrip().startswith("%"):
            continue
        cocok = RE_SUBFILE_AKTIF.match(baris)
        if cocok:
            aktif.add(cocok.group(1))

    for nomor in sorted(aktif):
        if not (CHAPTERS_DIR / nomor / "chapter.tex").exists():
            temuan.salah(f"main.tex: \\subfile bab {nomor} aktif tetapi berkasnya tidak ada.")

    temuan.info(
        f"main.tex: {len(aktif)} bab aktif; {len(bab_selesai)} direktori bab sudah terisi."
    )
    for nomor in sorted(set(bab_selesai) - aktif):
        temuan.info(f"main.tex: bab {nomor} sudah ditulis tetapi belum diaktifkan.")


def ambil_argumen(teks: str, perintah: str) -> list[str]:
    """Mengambil isi argumen berkurawal yang seimbang untuk sebuah perintah.

    Diperlukan karena ekspresi tetap tidak dapat menangani tanda kurung
    kurawal yang bersarang, misalnya \\code{-{}-user}.
    """
    hasil: list[str] = []
    awal = f"\\{perintah}{{"
    pos = 0
    while True:
        i = teks.find(awal, pos)
        if i < 0:
            break
        j = i + len(awal)
        dalam = 1
        buf: list[str] = []
        while j < len(teks):
            huruf = teks[j]
            if huruf == "{":
                dalam += 1
            elif huruf == "}":
                dalam -= 1
                if dalam == 0:
                    break
            buf.append(huruf)
            j += 1
        hasil.append("".join(buf))
        pos = j + 1
    return hasil


def periksa_isi_kode(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa isi \\code{...}, blok keluaran, dan keseimbangan kurung.

    Baik \\code maupun lingkungan kodekeluaran menampilkan teks apa adanya,
    sehingga perintah LaTeX dan karakter yang di-escape gaya LaTeX akan
    tercetak salah walaupun kompilasi berhasil. Pemeriksaan keseimbangan
    kurung kurawal menangkap kerusakan berkas yang lebih luas, misalnya
    akibat penyuntingan otomatis yang salah posisi.
    """
    for path, isi in sorted(berkas.items()):
        if path.name.startswith("uji"):
            continue

        # Bagian di luar blok keluaran program, yang diperlakukan sebagai LaTeX.
        blok = RE_KELUARAN.findall(isi)
        rentang = [cocok.span() for cocok in RE_KELUARAN.finditer(isi)]
        luar = RE_KELUARAN.sub("", isi)

        def di_dalam_keluaran(posisi: int) -> bool:
            return any(mulai <= posisi < akhir for mulai, akhir in rentang)

        for argumen in ambil_argumen(luar, "code"):
            for terlarang in TERLARANG_DI_CODE:
                if terlarang in argumen:
                    temuan.salah(
                        f"Penulisan: {rel(path)} memakai \\code{{{argumen}}} "
                        f"yang memuat '{terlarang}'. Isi \\code ditampilkan apa "
                        f"adanya, jadi tulis tanpa escape."
                    )

        for cocok in RE_CODE_RUSAK.finditer(isi):
            if di_dalam_keluaran(cocok.start()):
                continue
            baris = isi[:cocok.start()].count("\n") + 1
            cuplik = isi[max(0, cocok.start() - 15):cocok.end() + 25]
            cuplik = cuplik.replace("\n", " ")
            temuan.salah(
                f"Penulisan: {rel(path)} baris {baris} memuat fragmen \\cod "
                f"yang rusak pada '...{cuplik}...'."
            )

        # Keseimbangan kurung kurawal di luar blok keluaran dan komentar.
        bersih = "\n".join(RE_KOMENTAR.sub("", b) for b in luar.splitlines())
        bersih = bersih.replace("\\{", "").replace("\\}", "")
        buka, tutup = bersih.count("{"), bersih.count("}")
        if buka != tutup:
            temuan.salah(
                f"Penulisan: {rel(path)} kurung kurawalnya tidak seimbang "
                f"({buka} buka, {tutup} tutup). Berkas tampaknya rusak."
            )

        for satu_blok in blok:
            for terlarang in TERLARANG_DI_KELUARAN:
                if terlarang in satu_blok:
                    temuan.salah(
                        f"Penulisan: {rel(path)} memakai '{terlarang}' di dalam "
                        f"lingkungan kodekeluaran. Lingkungan itu verbatim, "
                        f"sehingga perintah LaTeX tercetak apa adanya."
                    )


def periksa_lingkungan(temuan: Temuan, berkas: dict[Path, str]) -> None:
    """Memeriksa kecocokan \\begin{...} dan \\end{...} pada setiap berkas.

    Kekurangan satu \\end atau kelebihan satu \\begin menimbulkan galat yang
    membingungkan jauh di bagian lain dokumen, sehingga lebih baik ditangkap
    di sini.
    """
    for path, isi in sorted(berkas.items()):
        # Perintah berargumen kosong, misalnya '\CPMK{}', mencetak teks tanpa
        # nomor dan biasanya menandakan argumen yang terlewat. Tidak
        # menimbulkan galat LaTeX, sehingga hanya dapat ditangkap di sini.
        for baris_no, baris in enumerate(isi.splitlines(), start=1):
            for perintah in RE_KOSONG.findall(baris):
                temuan.salah(
                    f"Penulisan: {rel(path)} baris {baris_no} memakai "
                    f"'\\{perintah}{{}}' dengan argumen kosong."
                )

        # Gaya penutup HTML '</namabox>' pernah beberapa kali terketik
        # sebagai ganti '\end{namabox}'. Pemeriksa kecocokan di bawah tidak
        # melihatnya, sebab bentuknya sama sekali berbeda; periksa tersendiri.
        for baris_no, baris in enumerate(isi.splitlines(), start=1):
            for nama in RE_TUTUP_HTML.findall(baris):
                temuan.salah(
                    f"Lingkungan: {rel(path)} baris {baris_no} memakai "
                    f"'</{nama}>'. LaTeX menuntut bentuk '\\end{{{nama}}}'."
                )

        buka = Counter(RE_BEGIN.findall(isi))
        tutup = Counter(RE_END.findall(isi))
        for nama in sorted(set(buka) | set(tutup)):
            jumlah_buka, jumlah_tutup = buka.get(nama, 0), tutup.get(nama, 0)
            if jumlah_buka != jumlah_tutup:
                temuan.salah(
                    f"Lingkungan: {rel(path)} memuat {jumlah_buka} "
                    f"\\begin{{{nama}}} tetapi {jumlah_tutup} \\end{{{nama}}}."
                )


def main() -> int:
    if not CHAPTERS_DIR.exists():
        print("Direktori chapters/ tidak ditemukan.")
        return 1

    temuan = Temuan()
    berkas = kumpulkan_tex()

    bab_selesai = periksa_kelengkapan(temuan)
    periksa_capaian(temuan, berkas)
    periksa_sitasi(temuan, berkas)
    periksa_rujukan_berkas(temuan, berkas)
    periksa_label(temuan, berkas)
    periksa_isi_kode(temuan, berkas)
    periksa_lingkungan(temuan, berkas)
    periksa_main(temuan, bab_selesai)

    print("=" * 68)
    print(" PEMERIKSAAN BUKU AJAR PENGANTAR PEMROGRAMAN GAME")
    print("=" * 68)
    print(f" Berkas .tex diperiksa : {len(berkas)}")
    print(f" Bab sudah ditulis     : {len(bab_selesai)}")
    print()

    if temuan.catatan:
        print("-- Keterangan " + "-" * 53)
        for pesan in temuan.catatan:
            print(f"   - {pesan}")
        print()

    if temuan.galat:
        print(f"-- Temuan ({len(temuan.galat)}) " + "-" * 50)
        for pesan in temuan.galat:
            print(f"   ! {pesan}")
        print()
        print("Hasil: ADA TEMUAN YANG PERLU DIPERBAIKI.")
        return 1

    print("Hasil: TIDAK ADA TEMUAN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

@echo off
REM =========================================================
REM  scripts/clean.bat
REM  Menghapus berkas bantu LaTeX (PDF tetap disimpan).
REM =========================================================

pushd "%~dp0.."

echo Membersihkan berkas bantu LaTeX...

latexmk -c main.tex

for /d %%D in (chapters\*) do (
    if exist "%%D\chapter.tex" (
        pushd "%%D"
        latexmk -c chapter.tex
        popd
    )
)

echo.
echo Selesai. Berkas .pdf tetap tersimpan.
popd

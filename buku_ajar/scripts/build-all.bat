@echo off
REM =========================================================
REM  scripts/build-all.bat
REM  Kompilasi seluruh buku ajar menjadi satu PDF.
REM =========================================================

pushd "%~dp0.."

echo ========================================
echo  Membangun Buku Ajar Pengantar Pemrograman Game
echo ========================================
echo.

latexmk -pdf main.tex

if errorlevel 1 (
    echo.
    echo Kompilasi gagal. Periksa main.log untuk keterangan kesalahan.
    popd
    exit /b 1
)

echo.
echo Selesai. Berkas keluaran: main.pdf
popd

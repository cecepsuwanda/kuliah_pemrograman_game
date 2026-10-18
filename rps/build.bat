@echo off
REM =========================================================
REM  build.bat
REM  Kompilasi dokumen RPS Pengantar Pemrograman Game
REM =========================================================

echo ========================================
echo  Membangun RPS Pengantar Pemrograman Game
echo ========================================
echo.

latexmk -pdf rps.tex

if errorlevel 1 (
    echo.
    echo Kompilasi gagal. Periksa rps.log untuk keterangan kesalahan.
    pause
    exit /b 1
)

echo.
echo Selesai. Berkas keluaran: rps.pdf
pause

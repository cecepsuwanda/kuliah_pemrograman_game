@echo off
REM =========================================================
REM  scripts/build-chapter.bat
REM  Kompilasi satu bab menjadi PDF tersendiri.
REM  Penggunaan: scripts\build-chapter.bat 04
REM =========================================================

setlocal

if "%~1"=="" (
    echo Penggunaan: build-chapter.bat ^<nomor bab^>
    echo Contoh     : build-chapter.bat 04
    exit /b 1
)

pushd "%~dp0..\chapters\%~1"

if not exist "chapter.tex" (
    echo Berkas chapter.tex tidak ditemukan pada chapters\%~1
    popd
    exit /b 1
)

echo ========================================
echo  Membangun Bab %~1
echo ========================================
echo.

latexmk -pdf chapter.tex
set HASIL=%errorlevel%

popd

if not "%HASIL%"=="0" (
    echo.
    echo Kompilasi bab %~1 gagal. Periksa chapters\%~1\chapter.log
    exit /b 1
)

echo.
echo Selesai. Keluaran: chapters\%~1\chapter.pdf

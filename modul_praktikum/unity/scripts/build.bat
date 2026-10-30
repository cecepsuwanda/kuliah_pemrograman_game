@echo off
rem =========================================================
rem  scripts/build.bat
rem  Mengompilasi modul menjadi gudang-artefak-unity.pdf
rem =========================================================
setlocal
cd /d "%~dp0.."

pdflatex -interaction=nonstopmode -halt-on-error -jobname=gudang-artefak-unity main.tex
if errorlevel 1 goto :gagal
pdflatex -interaction=nonstopmode -halt-on-error -jobname=gudang-artefak-unity main.tex
if errorlevel 1 goto :gagal

echo.
echo Selesai: gudang-artefak-unity.pdf
exit /b 0

:gagal
echo.
echo Kompilasi gagal. Periksa gudang-artefak-unity.log.
exit /b 1

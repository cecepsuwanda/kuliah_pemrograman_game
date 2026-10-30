@echo off
rem =========================================================
rem  scripts/build.bat
rem  Mengompilasi modul menjadi gudang-artefak-python.pdf
rem =========================================================
setlocal
cd /d "%~dp0.."

pdflatex -interaction=nonstopmode -halt-on-error -jobname=gudang-artefak-python main.tex
if errorlevel 1 goto :gagal
pdflatex -interaction=nonstopmode -halt-on-error -jobname=gudang-artefak-python main.tex
if errorlevel 1 goto :gagal

echo.
echo Selesai: gudang-artefak-python.pdf
exit /b 0

:gagal
echo.
echo Kompilasi gagal. Periksa gudang-artefak-python.log.
exit /b 1

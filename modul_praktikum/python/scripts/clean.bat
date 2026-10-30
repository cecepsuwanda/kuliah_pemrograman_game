@echo off
rem =========================================================
rem  scripts/clean.bat
rem  Menghapus berkas bantu kompilasi.
rem =========================================================
setlocal
cd /d "%~dp0.."

del /q gudang-artefak-python.aux gudang-artefak-python.log
del /q gudang-artefak-python.toc gudang-artefak-python.out
del /q main.aux main.log main.toc main.out
echo Berkas bantu dihapus.

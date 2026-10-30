@echo off
rem =========================================================
rem  scripts/clean.bat
rem  Menghapus berkas bantu kompilasi.
rem =========================================================
setlocal
cd /d "%~dp0.."

del /q gudang-artefak-unity.aux gudang-artefak-unity.log
del /q gudang-artefak-unity.toc gudang-artefak-unity.out
del /q main.aux main.log main.toc main.out
echo Berkas bantu dihapus.

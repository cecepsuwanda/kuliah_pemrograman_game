@echo off
echo ============================================================
echo Menghapus file hasil kompilasi LaTeX di folder buku_ajar...
echo ============================================================

pushd "%~dp0buku_ajar"

del /s *.aux
del /s *.log
del /s *.out
del /s *.toc
del /s *.lof
del /s *.lot
del /s *.bbl
del /s *.blg
del /s *.lol
del /s *.synctex.gz
del /s *.pdf

popd

echo.
echo Pembersihan selesai!
pause

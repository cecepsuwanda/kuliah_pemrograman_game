@echo off
echo ============================================================
echo Clean All Compilation Files - Game Programming Book
echo ============================================================
echo.

echo This will delete ALL LaTeX compilation files throughout the project.
echo Source files (.tex, .bib) will be preserved.
echo.
set /p confirm="Are you sure? (y/N): "

if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    pause
    exit /b
)

echo.
echo Cleaning all compilation files...

pushd "%~dp0"

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

popd

echo.
echo ============================================================
echo CLEANING COMPLETED!
echo ============================================================
echo.
echo All compilation files have been deleted.
echo Your source files are safe.
echo.
pause

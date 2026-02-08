@echo off
setlocal

echo ============================================================
echo Compile Single Chapter - Game Programming Book
echo ============================================================
echo.

if "%~1"=="" (
    echo Usage: compile_chapter.bat [chapter_number]
    echo Example: compile_chapter.bat 01
    echo.
    echo Available chapters:
    for %%F in (bab-01 bab-02 bab-03 bab-04 bab-05 bab-06 bab-07 bab-08 bab-09 bab-10 bab-11 bab-12 bab-13 bab-14 bab-15 bab-16) do (
        echo   %%F
    )
    echo.
    pause
    exit /b 1
)

set "ROOT_DIR=%~dp0"
set "OUTPUT_DIR=%ROOT_DIR%output"
set "BOOK_DIR=%ROOT_DIR%book"
set "CHAPTER_NUM=%~1"
set "CHAPTER_NAME=bab-%CHAPTER_NUM%"

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo Validating chapter %CHAPTER_NUM%...

if not exist "%BOOK_DIR%\chapters\%CHAPTER_NAME%\%CHAPTER_NAME%.tex" (
    echo ERROR: Chapter %CHAPTER_NAME% not found!
    echo Available chapters:
    for %%F in (bab-01 bab-02 bab-03 bab-04 bab-05 bab-06 bab-07 bab-08 bab-09 bab-10 bab-11 bab-12 bab-13 bab-14 bab-15 bab-16) do (
        if exist "%BOOK_DIR%\chapters\%%F\%%F.tex" echo   %%F
    )
    echo.
    pause
    exit /b 1
)

echo Chapter %CHAPTER_NAME% found, starting compilation...
echo.

pushd "%BOOK_DIR%\chapters\%CHAPTER_NAME%"

echo.
echo ============================================================
echo Compiling %CHAPTER_NAME%
echo ============================================================
echo.

echo Stage 1: pdflatex -initial...
pdflatex -interaction=nonstopmode -halt-on-error "%CHAPTER_NAME%.tex"
if errorlevel 1 goto :compilation_failed

echo Stage 2: bibtex...
bibtex "%CHAPTER_NAME%"
if errorlevel 1 (
    echo Warning: bibtex failed, continuing...
)

echo Stage 3: pdflatex -crossref...
pdflatex -interaction=nonstopmode -halt-on-error "%CHAPTER_NAME%.tex"
if errorlevel 1 goto :compilation_failed

echo Stage 4: pdflatex -final...
pdflatex -interaction=nonstopmode "%CHAPTER_NAME%.tex"
if errorlevel 1 goto :compilation_failed

echo.
echo ============================================================
echo COMPILATION SUCCESSFUL!
echo ============================================================
echo.

if exist "%CHAPTER_NAME%.pdf" (
    echo Moving %CHAPTER_NAME%.pdf to output directory...
    move /y "%CHAPTER_NAME%.pdf" "%OUTPUT_DIR%\"
    echo Success! PDF saved to: %OUTPUT_DIR%\%CHAPTER_NAME%.pdf
) else (
    echo ERROR: PDF was not generated
    goto :compilation_failed
)

goto :cleanup

:compilation_failed
echo.
echo ============================================================
echo COMPILATION FAILED!
echo ============================================================
echo.
echo Check the log file for errors: %CHAPTER_NAME%.log
echo.
echo Common issues to check:
echo   1. Missing LaTeX packages in preamble.tex
echo   2. Syntax errors in .tex files
echo   3. Missing bibliography entries
echo   4. File path issues
echo   5. Missing section files
echo.

:cleanup
echo.
echo Cleaning intermediate files...
for %%E in (aux bbl blg bcf out toc lof lot fls fdb_latexmk nav snm vrb idx ilg ind acn acr alg glg glo gls ist xdy run.xml synctex pdfsync synctex.gz log) do (
    if exist "%%E" del /s /q "%%E" 2>nul
)

popd

echo.
echo Operation completed.
pause
exit /b 0

@echo off
setlocal

echo ============================================================
echo Quick Compilation - Game Programming Book
echo ============================================================
echo.

set "ROOT_DIR=%~dp0"
set "OUTPUT_DIR=%ROOT_DIR%output"
set "BOOK_DIR=%ROOT_DIR%book"

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo 1. Complete Book (main.pdf)
echo 2. All Chapters (bab-01.pdf to bab-16.pdf)
echo 3. Single Chapter
echo 4. Exit
echo.
set /p choice="Select option (1-4): "

if "%choice%"=="1" goto :compile_book
if "%choice%"=="2" goto :compile_chapters
if "%choice%"=="3" goto :compile_single
if "%choice%"=="4" goto :end
goto :invalid

:compile_book
echo.
echo Compiling complete book...
pushd "%BOOK_DIR%"
pdflatex -interaction=nonstopmode -output-directory="%OUTPUT_DIR%" main.tex
if errorlevel 1 (
    echo ERROR: Book compilation failed!
) else (
    echo SUCCESS: main.pdf created in %OUTPUT_DIR%
)
popd
goto :end

:compile_chapters
echo.
echo Compiling all chapters...
pushd "%BOOK_DIR%\chapters"
for %%F in (bab-01 bab-02 bab-03 bab-04 bab-05 bab-06 bab-07 bab-08 bab-09 bab-10 bab-11 bab-12 bab-13 bab-14 bab-15 bab-16) do (
    echo Compiling %%F...
    if exist "%%F\%%F.tex" (
        pushd "%%F"
        pdflatex -interaction=nonstopmode "%%F.tex"
        if errorlevel 1 (
            echo ERROR: %%F failed!
        ) else (
            if exist "%%F.pdf" move "%%F.pdf" "%OUTPUT_DIR%\"
            echo SUCCESS: %%F.pdf
        )
        popd
    ) else (
        echo WARNING: %%F not found!
    )
)
popd
goto :end

:compile_single
echo.
set /p chapter="Enter chapter number (01-16): "
set "CHAPTER_NAME=bab-%chapter%"

if not exist "%BOOK_DIR%\chapters\%CHAPTER_NAME%\%CHAPTER_NAME%.tex" (
    echo ERROR: Chapter %CHAPTER_NAME% not found!
    goto :end
)

echo Compiling %CHAPTER_NAME%...
pushd "%BOOK_DIR%\chapters\%CHAPTER_NAME%"
pdflatex -interaction=nonstopmode "%CHAPTER_NAME%.tex"
if errorlevel 1 (
    echo ERROR: %CHAPTER_NAME% compilation failed!
) else (
    if exist "%CHAPTER_NAME%.pdf" move "%CHAPTER_NAME%.pdf" "%OUTPUT_DIR%\"
    echo SUCCESS: %CHAPTER_NAME%.pdf created!
)
popd
goto :end

:invalid
echo Invalid choice!
goto :end

:end
echo.
echo ============================================================
echo Operation completed!
echo Output directory: %OUTPUT_DIR%
echo ============================================================
pause

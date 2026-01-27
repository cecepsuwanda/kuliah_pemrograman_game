@echo off
REM ============================================================================
REM PROFESSIONAL LaTeX BOOK COMPILER
REM Author  : Buku Ajar Pemrograman Game
REM Version : 2.0 Professional
REM ============================================================================

setlocal EnableExtensions EnableDelayedExpansion

REM =========================
REM CONFIGURATION
REM =========================
set "BASE_DIR=%~dp0"
set "BOOK_DIR=%BASE_DIR%book"
set "OUTPUT_DIR=%BASE_DIR%output"
set "MAX_CHAPTER=13"
set "MAIN_FILE=main"

REM =========================
REM STATE VARIABLES
REM =========================
set "MODE=all"
set "CHAPTERS="
set "RANGE_START="
set "RANGE_END="
set "ERROR_FLAG=0"

REM =========================
REM ENTRY POINT
REM =========================
if "%~1"=="" goto :MENU
call :PARSE_ARGS %*
goto :START

REM =========================
REM MENU MODE
REM =========================
:MENU
cls
echo ==================================================
echo        LaTeX BOOK COMPILER - PROFESSIONAL
echo ==================================================
echo.
echo [1] Compile ALL chapters
echo [2] Compile specific chapters (e.g. 1 3 5)
echo [3] Compile chapter range (e.g. 1-5)
echo [0] Exit
echo.
set /p "CHOICE=Select option: "

if "%CHOICE%"=="1" goto :START
if "%CHOICE%"=="2" goto :INPUT_LIST
if "%CHOICE%"=="3" goto :INPUT_RANGE
if "%CHOICE%"=="0" goto :END
goto :MENU

:INPUT_LIST
set /p "TMP_LIST=Enter chapters (space separated): "
call :PARSE_LIST %TMP_LIST%
goto :START

:INPUT_RANGE
set /p "TMP_RANGE=Enter range (start-end): "
call :PARSE_RANGE %TMP_RANGE%
goto :START

REM =========================
REM ARGUMENT PARSER
REM =========================
:PARSE_ARGS
if "%~1"=="" exit /b
if /i "%~1"=="all" exit /b

echo %~1 | findstr /R "^[0-9][0-9]*-[0-9][0-9]*$" >nul && (
    call :PARSE_RANGE %~1
    exit /b
)

call :PARSE_LIST %*
exit /b

:PARSE_RANGE
for /f "tokens=1,2 delims=-" %%a in ("%~1") do (
    set "RANGE_START=%%a"
    set "RANGE_END=%%b"
    set "MODE=range"
)
exit /b

:PARSE_LIST
set "MODE=chapters"
for %%a in (%*) do (
    set "ARG=%%a"
    if /i "!ARG:~0,2!"=="ch" set "ARG=!ARG:~2!"
    if "!ARG:~0,1!"=="0" set "ARG=!ARG:~1!"

    echo !ARG! | findstr /R "^[0-9][0-9]*$" >nul || goto :NEXT_ARG
    if !ARG! GEQ 1 if !ARG! LEQ %MAX_CHAPTER% (
        set "CHAPTERS=!CHAPTERS! !ARG!"
    )
:NEXT_ARG
)
exit /b

REM =========================
REM START COMPILATION
REM =========================
:START
cls
echo ==================================================
echo STARTING COMPILATION...
echo ==================================================

if not exist "%BOOK_DIR%" (
    echo ERROR: Folder book not found.
    goto :FAIL
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

cd /d "%BOOK_DIR%" || goto :FAIL

call :CLEAN

if "%MODE%"=="all" call :COMPILE_MAIN
if "%MODE%"=="range" call :COMPILE_RANGE
if "%MODE%"=="chapters" call :COMPILE_LIST

if %ERROR_FLAG%==0 (
    call :CLEAN
    echo.
    echo SUCCESS: Compilation completed.
) else (
    echo.
    echo FAILED: Errors detected. Check .log files.
)
goto :END

REM =========================
REM CLEAN TEMP FILES
REM =========================
:CLEAN
for /r %%f in (*.aux *.log *.out *.toc *.lof *.lot *.bbl *.bcf *.blg *.run.xml *.synctex.gz *.fdb_latexmk *.fls *.idx *.ilg *.ind *.glo *.gls *.glg) do del /q "%%f" 2>nul
exit /b

REM =========================
REM COMPILE MAIN BOOK
REM =========================
:COMPILE_MAIN
echo [INFO] Compiling main book...
call :LATEX_PIPELINE %MAIN_FILE%
if errorlevel 1 (
    set "ERROR_FLAG=1"
    exit /b
)
if exist "%MAIN_FILE%.pdf" (
    move /y "%MAIN_FILE%.pdf" "%OUTPUT_DIR%\Buku_Ajar_Pemrograman_Game.pdf" >nul
)
exit /b

REM =========================
REM COMPILE RANGE
REM =========================
:COMPILE_RANGE
for /l %%i in (%RANGE_START%,1,%RANGE_END%) do call :COMPILE_CHAPTER %%i
exit /b

REM =========================
REM COMPILE LIST
REM =========================
:COMPILE_LIST
for %%c in (%CHAPTERS%) do call :COMPILE_CHAPTER %%c
exit /b

REM =========================
REM COMPILE SINGLE CHAPTER
REM =========================
:COMPILE_CHAPTER
set "NUM=%~1"
if %NUM% LSS 10 (set "CH=ch0%NUM%") else set "CH=ch%NUM%"
set "DIR=chapters\%CH%"

if not exist "%DIR%\%CH%.tex" (
    echo [SKIP] Chapter %NUM% not found.
    exit /b
)

echo [INFO] Compiling chapter %NUM%...
pushd "%DIR%"
call :LATEX_PIPELINE %CH%
popd

if exist "%DIR%\%CH%.pdf" (
    move /y "%DIR%\%CH%.pdf" "%OUTPUT_DIR%\Bab_%NUM%_%CH%.pdf" >nul
)
exit /b

REM =========================
REM LATEX PIPELINE
REM =========================
:LATEX_PIPELINE
set "FILE=%~1"

pdflatex -interaction=nonstopmode -halt-on-error "%FILE%.tex" >nul || exit /b 1
biber "%FILE%" >nul 2>&1
makeglossaries "%FILE%" >nul 2>&1
pdflatex -interaction=nonstopmode -halt-on-error "%FILE%.tex" >nul || exit /b 1
pdflatex -interaction=nonstopmode -halt-on-error "%FILE%.tex" >nul || exit /b 1

exit /b 0

REM =========================
REM FAIL HANDLER
REM =========================
:FAIL
echo ERROR: Fatal error occurred.
set "ERROR_FLAG=1"

REM =========================
REM END
REM =========================
:END
echo ==================================================
echo Process finished.
echo ==================================================
pause
endlocal
exit /b

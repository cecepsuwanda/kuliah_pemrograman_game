@echo off
rem =========================================================
rem  ppt/build.bat
rem  Mengompilasi keempat belas presentasi menjadi PDF.
rem  Jalankan dari folder mana pun; skrip berpindah sendiri.
rem =========================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"

set FAILED=0
set COUNT=0

for %%F in (??-*.tex) do (
    set /a COUNT+=1
    echo [%%~nF] mengompilasi ...
    pdflatex -interaction=nonstopmode -halt-on-error "%%F" > "%%~nF.build.log" 2>&1
    if errorlevel 1 (
        echo    GAGAL - lihat %%~nF.build.log
        set FAILED=1
    ) else (
        pdflatex -interaction=nonstopmode -halt-on-error "%%F" > "%%~nF.build.log" 2>&1
        if errorlevel 1 (
            echo    GAGAL pada proses kedua - lihat %%~nF.build.log
            set FAILED=1
        ) else (
            echo    OK
        )
    )
)

echo.
if "%FAILED%"=="1" (
    echo Ada berkas yang gagal dikompilasi. Periksa berkas .build.log.
    exit /b 1
)
echo Selesai: %COUNT% presentasi berhasil dikompilasi.
exit /b 0

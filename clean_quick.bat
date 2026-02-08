@echo off
echo ============================================================
echo Quick Clean - Game Programming Book
echo ============================================================
echo.

echo 1. Clean all compilation files
echo 2. Clean book directory only
echo 3. Clean chapters only
echo 4. Clean output directory only
echo 5. Exit
echo.
set /p choice="Select option (1-5): "

if "%choice%"=="1" goto :clean_all
if "%choice%"=="2" goto :clean_book
if "%choice%"=="3" goto :clean_chapters
if "%choice%"=="4" goto :clean_output
if "%choice%"=="5" goto :end
goto :invalid

:clean_all
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
goto :success

:clean_book
echo.
echo Cleaning book directory only...
pushd "%~dp0book"
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
goto :success

:clean_chapters
echo.
echo Cleaning chapters only...
pushd "%~dp0book\chapters"
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
goto :success

:clean_output
echo.
echo Cleaning output directory only...
pushd "%~dp0output"
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
goto :success

:invalid
echo Invalid choice!
goto :end

:success
echo.
echo ============================================================
echo CLEANING COMPLETED!
echo ============================================================
echo.

:end
pause
exit /b 0

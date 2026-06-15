@echo off
echo ============================================
<<<<<<< HEAD
echo   MorphX — Single File Release Build
=======
echo  FileConverter — PyInstaller Build Script
>>>>>>> d26ac61649f2aceacca66d74e9b1b5fe3600d0f0
echo ============================================

call venv\Scripts\activate

<<<<<<< HEAD
echo.
echo [1/3] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo [2/3] Checking poppler_bin folder...
if not exist poppler_bin (
    echo ERROR: poppler_bin folder not found!
    echo Run this first:
    echo   xcopy /E /I "E:\Python\AdvancePython\poppler-26.02.0\Library\bin" "poppler_bin"
    pause
    exit /b 1
)

echo [3/3] Building single-file executable...
pyinstaller converter.spec --clean --noconfirm

echo.
if exist dist\MorphX.exe (
    echo ============================================
    echo  BUILD SUCCESSFUL
    echo  Output: dist\MorphX.exe
    echo  Size:
    for %%A in (dist\MorphX.exe) do echo    %%~zA bytes
    echo ============================================
=======
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building executable...
pyinstaller converter.spec --clean --noconfirm

echo.
if exist dist\FileConverter\FileConverter.exe (
    echo BUILD SUCCESSFUL
    echo Output: dist\FileConverter\FileConverter.exe
>>>>>>> d26ac61649f2aceacca66d74e9b1b5fe3600d0f0
) else (
    echo BUILD FAILED — check errors above
)
pause
@echo off
echo ============================================
echo  FileConverter — PyInstaller Build Script
echo ============================================

call venv\Scripts\activate

echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building executable...
pyinstaller converter.spec --clean --noconfirm

echo.
if exist dist\FileConverter\FileConverter.exe (
    echo BUILD SUCCESSFUL
    echo Output: dist\FileConverter\FileConverter.exe
) else (
    echo BUILD FAILED — check errors above
)
pause
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

added_files = [
    ('assets', 'assets'),
    ('app', 'app'),
]

hidden_imports = [
    'comtypes.server',
    'comtypes.client',
    'comtypes.automation',
    'win32com.client',
    'win32api',
    'win32con',
    'pywintypes',
    'pdf2docx',
    'pdf2image',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'pptx',
    'pptx.util',
    'pptx.enum.text',
    'docx',
    'docx.shared',
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
]

hidden_imports += collect_submodules('pdf2docx')
hidden_imports += collect_submodules('pptx')
hidden_imports += collect_submodules('docx')
hidden_imports += collect_submodules('comtypes')

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FileConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FileConverter',
)
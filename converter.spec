# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

hidden_imports = [
    'comtypes.server',
    'comtypes.client',
    'comtypes.automation',
    'comtypes._gen',
    'win32com.client',
    'win32api',
    'win32con',
    'win32process',
    'pywintypes',
    'pdf2docx',
    'pdf2image',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFilter',
    'PIL.ImageFont',
    'pptx',
    'pptx.util',
    'pptx.oxml',
    'pptx.enum.text',
    'pptx.dml.color',
    'docx',
    'docx.shared',
    'docx.oxml',
    'docx.enum.text',
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.sip',
]

hidden_imports += collect_submodules('pdf2docx')
hidden_imports += collect_submodules('pptx')
hidden_imports += collect_submodules('docx')
hidden_imports += collect_submodules('comtypes')
hidden_imports += collect_submodules('PIL')

datas = [
    ('assets', 'assets'),
    ('app', 'app'),
    ('poppler_bin', 'poppler_bin'),
]

datas += collect_data_files('pdf2docx')
datas += collect_data_files('pptx')
datas += collect_data_files('docx')

a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'pandas', 'notebook'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MorphX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
    onefile=True,
)
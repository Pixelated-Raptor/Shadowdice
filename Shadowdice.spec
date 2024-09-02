# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('Assets/Black_Die_Dotted/*.png', 'Assets/Black_Die_Dotted/'), ('Assets/Black_Die_Numbered/*.png', 'Assets/Black_Die_Numbered/'), ('Assets/Coloured_Die_Dotted/*.png', 'Assets/Coloured_Die_Dotted'), ('Assets/Coloured_Die_Numbered/*.png', 'Assets/Coloured_Die_Numbered'), ('Assets/icon.ico', 'Assets/'), ('lang/*.json', 'lang')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Shadowdice',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Assets\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Shadowdice',
)

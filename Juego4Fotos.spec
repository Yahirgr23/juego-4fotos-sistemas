# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('backups', 'backups'), ('clienteassets', 'clientassets'), ('clienteassetsfonts', 'clienteassetsfonts'), ('clienteassetsimages', 'clienteassetsimages'), ('clienteassetssounds', 'clienteassetssounds'), ('custom_levels', 'custom_levels'), ('downloaded_levels', 'downloaded_levels'), ('temp', 'temp'), ('test_images', 'test_images'), ('game_config.json', '.'), ('Procfile', '.'), ('README.md', '.'), ('requirements.txt', '.')],
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
    name='Juego4Fotos',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Juego4Fotos',
)

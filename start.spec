# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

appConfig = {
    'name': 'Right Click Helper',
    'icon': './src/resource/image/icon/right-click-helper.ico',

    'entry-script': ['./src/rightClickHelper/app.py']
}

datas = [
    ('./src/resource/', './src/resource/'),
    ('./lib/dll/Python.Runtime.dll', '.'),
    ('./LICENSE', '.'),
    ('./README.md', '.'),
    ('./CHANGELOG.en-US.md', '.'),
    ('./CHANGELOG.zh-CN.md', '.'),
]

analysis = Analysis(
    appConfig['entry-script'],
    pathex=['./'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
    analysis.pure, analysis.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz, analysis.scripts,
    [],
    exclude_binaries=True,
    name=appConfig['name'],
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    uac_admin=True,
    upx_exclude=['./upx-3.96'],
    console=False,
    icon=appConfig['icon']
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=['./upx-3.96'],
    name=appConfig['name']
)

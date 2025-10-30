# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
用于将链接提取工具打包成独立的exe程序
"""

block_cipher = None

a = Analysis(
    ['链接提取工具_GUI版.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 如果需要包含其他数据文件，在这里添加
        # ('README.md', '.'),
    ],
    hiddenimports=[
        'pandas',
        'requests',
        'bs4',
        'openpyxl',
        'playwright',
        'playwright.sync_api',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积
        'matplotlib',
        'numpy.f2py',
        'scipy',
        'IPython',
        'jupyter',
    ],
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
    name='链接提取工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，在这里指定路径
)


# -*- mode: python ; coding: utf-8 -*-
"""
单目录模式打包配置
优点：解压到固定目录，避免权限问题
缺点：生成文件夹，不是单个exe
"""

block_cipher = None
import sys
import os
from pathlib import Path

a = Analysis(
    ['链接提取工具_GUI版.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'playwright',
        'playwright.sync_api',
        'requests',
        'bs4',
        'openpyxl',
        'pandas',
        'lxml',
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
    [],  # 注意：这里为空，使用COLLECT
    exclude_binaries=True,  # 单目录模式关键参数
    name='链接提取工具',
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
    icon=None,
    uac_admin=False,  # 单目录模式不需要管理员权限
    uac_uiaccess=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='链接提取工具',
)


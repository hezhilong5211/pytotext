# -*- mode: python ; coding: utf-8 -*-
"""
单目录模式打包配置
优点：解压到固定目录，避免权限问题
缺点：生成文件夹，不是单个exe
"""

block_cipher = None
import sys
import os
import glob
from pathlib import Path

# 查找Playwright浏览器路径（与build_exe.spec相同）
playwright_browsers = []

if sys.platform == 'win32':
    possible_paths = [
        os.path.expanduser('~/AppData/Local/ms-playwright'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'ms-playwright'),
        'C:/Users/*/AppData/Local/ms-playwright',
    ]
else:
    possible_paths = [
        os.path.expanduser('~/.cache/ms-playwright'),
        os.path.expanduser('~/Library/Caches/ms-playwright'),
    ]

print("Searching for Playwright browsers (onedir)...")
for base_path in possible_paths:
    if '*' in base_path:
        expanded_paths = glob.glob(base_path)
    else:
        expanded_paths = [base_path] if os.path.exists(base_path) else []
    
    for expanded_path in expanded_paths:
        if os.path.exists(expanded_path):
            print(f"  Checking path: {expanded_path}")
            chromium_dirs = glob.glob(os.path.join(expanded_path, 'chromium-*'))
            if chromium_dirs:
                chromium_path = sorted(chromium_dirs)[-1]
                playwright_browsers.append((chromium_path, 'playwright_browsers/chromium'))
                print(f"[OK] Found Playwright Chromium: {chromium_path}")
                try:
                    size_mb = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(chromium_path) for filename in filenames) / 1024 / 1024
                    print(f"     Size: {size_mb:.1f} MB")
                except:
                    print("     Size: (unable to calculate)")
                break
        if playwright_browsers:
            break
    if playwright_browsers:
        break

if not playwright_browsers:
    print("[WARNING] Playwright browser not found for onedir build")
else:
    print(f"[INFO] Will package {len(playwright_browsers)} browser component(s)")

a = Analysis(
    ['链接提取工具_GUI版.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含Playwright浏览器
        *playwright_browsers,
    ],
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
    upx=False,  # 禁用upx，避免压缩大文件失败
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
    upx=False,  # 禁用upx，避免压缩大文件失败
    upx_exclude=[],
    name='链接提取工具',
)


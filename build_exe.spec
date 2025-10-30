# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包配置文件
用于将链接提取工具打包成独立的exe程序
"""

block_cipher = None

import os
import glob
import sys

# 查找Playwright浏览器路径
playwright_browsers = []

# Windows路径处理
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

print("Searching for Playwright browsers...")
for base_path in possible_paths:
    # 展开通配符路径
    if '*' in base_path:
        expanded_paths = glob.glob(base_path)
    else:
        expanded_paths = [base_path] if os.path.exists(base_path) else []
    
    for expanded_path in expanded_paths:
        if os.path.exists(expanded_path):
            print(f"  Checking path: {expanded_path}")
            chromium_dirs = glob.glob(os.path.join(expanded_path, 'chromium-*'))
            if chromium_dirs:
                # 找到最新版本的chromium
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
    print("[WARNING] Playwright browser not found")
    print("          The generated exe will require manual browser installation")
else:
    print(f"[INFO] Will package {len(playwright_browsers)} browser component(s)")

a = Analysis(
    ['链接提取工具_GUI版.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 包含Playwright浏览器
        *playwright_browsers,
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
    upx=False,  # 禁用upx，避免压缩大文件失败
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，在这里指定路径
    uac_admin=True,  # 请求管理员权限
    uac_uiaccess=False,
)


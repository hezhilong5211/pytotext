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

print("🔍 搜索Playwright浏览器...")
for base_path in possible_paths:
    # 展开通配符路径
    if '*' in base_path:
        expanded_paths = glob.glob(base_path)
    else:
        expanded_paths = [base_path] if os.path.exists(base_path) else []
    
    for expanded_path in expanded_paths:
        if os.path.exists(expanded_path):
            print(f"  检查路径: {expanded_path}")
            chromium_dirs = glob.glob(os.path.join(expanded_path, 'chromium-*'))
            if chromium_dirs:
                # 找到最新版本的chromium
                chromium_path = sorted(chromium_dirs)[-1]
                playwright_browsers.append((chromium_path, 'playwright_browsers/chromium'))
                print(f"✅ 找到Playwright Chromium: {chromium_path}")
                print(f"   大小: {sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(chromium_path) for filename in filenames) / 1024 / 1024:.1f} MB")
                break
        if playwright_browsers:
            break
    if playwright_browsers:
        break

if not playwright_browsers:
    print("⚠️ 警告: 未找到Playwright浏览器")
    print("   将生成不含浏览器的exe，使用时需要手动安装")
else:
    print(f"📦 将打包 {len(playwright_browsers)} 个浏览器组件")

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


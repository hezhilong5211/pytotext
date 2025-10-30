@echo off
chcp 65001 >nul
title 检查打包是否包含浏览器

echo ======================================================
echo   检查打包是否包含浏览器
echo ======================================================
echo.

echo [1/4] 检查本地浏览器是否存在...
echo ------------------------------------------------------
if exist "%LOCALAPPDATA%\ms-playwright\chromium-*" (
    echo ✅ 本地浏览器存在
    dir "%LOCALAPPDATA%\ms-playwright" /b
) else (
    echo ❌ 本地浏览器不存在
    echo 请先运行: python -m playwright install chromium
    pause
    exit /b 1
)
echo.

echo [2/4] 查看浏览器详细路径...
echo ------------------------------------------------------
dir "%LOCALAPPDATA%\ms-playwright\chromium-*" /s /b | findstr "chrome.exe" | head -1
echo.

echo [3/4] 检查dist目录的exe文件大小...
echo ------------------------------------------------------
if exist "dist\链接提取工具.exe" (
    echo 文件: dist\链接提取工具.exe
    dir "dist\链接提取工具.exe" | findstr "链接提取工具.exe"
    echo.
    echo 说明:
    echo   - 如果大小约30MB   = 浏览器没打包进去 ❌
    echo   - 如果大小约130MB+ = 浏览器已打包进去 ✅
) else (
    echo ⚠️ dist\链接提取工具.exe 不存在，请先打包
)
echo.

echo [4/4] 测试打包检测（模拟pyinstaller）...
echo ------------------------------------------------------
python -c "import os, glob; paths = [os.path.expanduser('~/AppData/Local/ms-playwright')]; [print(f'Found: {p}') for base in paths for p in glob.glob(os.path.join(base, 'chromium-*')) if os.path.exists(base)]"
echo.

echo ======================================================
echo   诊断完成
echo ======================================================
echo.
echo 如果浏览器存在但exe只有30MB，说明打包时没有包含。
echo 请查看打包日志，看是否有 [OK] Found Playwright Chromium 的提示。
echo.
pause


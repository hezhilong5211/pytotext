@echo off
title Check Browser in Package

echo ======================================================
echo   Check Browser in Package
echo ======================================================
echo.

echo [1/4] Check local browser...
echo ------------------------------------------------------
if exist "%LOCALAPPDATA%\ms-playwright\chromium-*" (
    echo OK: Browser exists
    dir "%LOCALAPPDATA%\ms-playwright" /b
) else (
    echo ERROR: Browser not found
    echo Please run: python -m playwright install chromium
    pause
    exit /b 1
)
echo.

echo [2/4] Browser path...
echo ------------------------------------------------------
dir "%LOCALAPPDATA%\ms-playwright\chromium-*" /b
echo.

echo [3/4] Check exe size...
echo ------------------------------------------------------
if exist "dist\链接提取工具.exe" (
    echo File: dist\链接提取工具.exe
    dir "dist\链接提取工具.exe"
    echo.
    echo Note:
    echo   - Size about 30MB  = Browser NOT included
    echo   - Size about 130MB = Browser included
) else (
    echo WARNING: dist\链接提取工具.exe not found
    echo Please package first
)
echo.

echo [4/4] Test detection...
echo ------------------------------------------------------
python -c "import os, glob; paths = [os.path.expanduser('~/AppData/Local/ms-playwright')]; [print(f'Found: {p}') for base in paths for p in glob.glob(os.path.join(base, 'chromium-*')) if os.path.exists(base)]"
echo.

echo ======================================================
echo   Done
echo ======================================================
echo.
echo If browser exists but exe is only 30MB,
echo it means browser was not packaged.
echo.
pause


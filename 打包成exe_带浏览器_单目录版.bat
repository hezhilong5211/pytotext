@echo off
title Package to EXE (OneDir Version)

echo ======================================================
echo   Package to EXE (OneDir - Include Browser)
echo ======================================================
echo.
echo Press any key to start...
pause

echo.
echo [1/4] Check Python...
echo ------------------------------------------------------
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)
echo.

echo [2/4] Check PyInstaller...
echo ------------------------------------------------------
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found, installing...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
pyinstaller --version
echo.

echo [3/4] Check local browser...
echo ------------------------------------------------------
if exist "%LOCALAPPDATA%\ms-playwright\chromium-*" (
    echo OK: Browser found
    dir "%LOCALAPPDATA%\ms-playwright" /b | findstr chromium
) else (
    echo WARNING: Browser not found
    echo Please run: python -m playwright install chromium
)
echo.

echo [4/4] Start packaging...
echo ------------------------------------------------------
pyinstaller build_exe_onedir.spec --clean --log-level INFO
echo.

echo ======================================================
echo Check result...
echo ======================================================
if exist "dist\链接提取工具" (
    echo OK: Package successful
    echo.
    dir "dist\链接提取工具" /b
    echo.
    if exist "dist\链接提取工具\playwright_browsers" (
        echo OK: Browser included
    ) else (
        echo WARNING: Browser NOT included
    )
) else (
    echo ERROR: Package failed
)

echo.
echo ======================================================
echo   Done
echo ======================================================
pause


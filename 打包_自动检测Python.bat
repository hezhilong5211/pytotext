@echo off
title Package EXE (Auto Detect Python)

echo ======================================================
echo   Package EXE - Auto Detect Python
echo ======================================================
echo.

REM 尝试找到Python命令
set PYTHON_CMD=

echo Testing python commands...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :found_python
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :found_python
)

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py -3
    goto :found_python
)

echo ERROR: Python not found
echo.
echo Please check:
echo   1. Python installed? Download from https://www.python.org/
echo   2. Added to PATH?
echo   3. Try running: python --version  or  py --version
echo.
pause
exit /b 1

:found_python
echo OK: Found Python command: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

echo [1/3] Check PyInstaller...
echo ------------------------------------------------------
%PYTHON_CMD% -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found, installing...
    %PYTHON_CMD% -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo OK: PyInstaller installed
echo.

echo [2/3] Check browser...
echo ------------------------------------------------------
if exist "%LOCALAPPDATA%\ms-playwright\chromium-*" (
    echo OK: Browser found
    dir "%LOCALAPPDATA%\ms-playwright" /b | findstr chromium
) else (
    echo WARNING: Browser not found
    echo Installing browser...
    %PYTHON_CMD% -m playwright install chromium
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install browser
        pause
        exit /b 1
    )
)
echo.

echo [3/3] Start packaging...
echo ------------------------------------------------------
echo Using command: %PYTHON_CMD% -m PyInstaller
%PYTHON_CMD% -m PyInstaller build_exe_onedir.spec --clean --log-level INFO
echo.

echo ======================================================
echo Check result...
echo ======================================================
if exist "dist\链接提取工具" (
    echo OK: Package successful
    echo.
    echo Files:
    dir "dist\链接提取工具" /b
    echo.
    if exist "dist\链接提取工具\playwright_browsers" (
        echo OK: Browser included
        echo Size:
        dir "dist\链接提取工具\playwright_browsers" | findstr "个文件"
    ) else (
        echo WARNING: Browser NOT included
    )
    echo.
    echo ======================================================
    echo   SUCCESS
    echo ======================================================
    echo.
    echo Packaged to: dist\链接提取工具\
    echo.
    echo Usage:
    echo   1. Copy the entire folder to target PC
    echo   2. Run 链接提取工具.exe
    echo.
) else (
    echo ERROR: Package failed
    echo Please check the log above
)

echo.
pause


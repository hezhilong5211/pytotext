@echo off
REM ============================================
REM 链接提取工具 - Windows 打包脚本
REM ============================================

echo ========================================
echo 链接提取工具 - 打包成 EXE
echo ========================================
echo.

REM 检查是否安装了依赖
echo [1/4] 检查依赖...
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到 tkinter，请确保安装了完整的 Python
    pause
    exit /b 1
)

echo 依赖检查通过
echo.

REM 安装/更新打包依赖
echo [2/4] 安装/更新依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)
echo.

REM 安装 Playwright 浏览器（可选）
echo [3/4] 安装 Playwright 浏览器（用于百度/抖音）...
python -m playwright install chromium
if %errorlevel% neq 0 (
    echo 警告: Playwright 安装失败，部分功能可能受限
)
echo.

REM 打包成 EXE
echo [4/4] 开始打包...
pyinstaller build_exe.spec --clean

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 打包成功！
    echo ========================================
    echo.
    echo EXE 文件位置: dist\链接提取工具.exe
    echo.
    echo 您可以将 dist 文件夹中的所有内容复制到其他电脑使用
    echo.
) else (
    echo.
    echo ========================================
    echo 打包失败！
    echo ========================================
    echo.
    echo 请检查错误信息
)

pause


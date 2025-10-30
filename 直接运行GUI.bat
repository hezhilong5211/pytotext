@echo off
REM ============================================
REM 快速启动 - Windows
REM ============================================

echo 正在启动链接提取工具...
python 链接提取工具_GUI版.py

if %errorlevel% neq 0 (
    echo.
    echo 启动失败，请确保已安装所需依赖：
    echo pip install -r requirements.txt
    pause
)


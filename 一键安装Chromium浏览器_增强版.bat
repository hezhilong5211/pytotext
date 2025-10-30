@echo off
chcp 65001 >nul
title 一键安装Chromium浏览器 - 增强版

echo ======================================================
echo   链接提取工具 - Chromium浏览器一键安装
echo ======================================================
echo.
echo 本脚本将自动安装Playwright Chromium浏览器
echo 安装位置: %LOCALAPPDATA%\ms-playwright
echo.
echo 按任意键开始安装...
pause >nul

echo.
echo [1/4] 检查Python环境...
echo ------------------------------------------------------
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未找到Python环境
    echo.
    echo 请先安装Python，或者使用打包好的exe版本。
    echo 如果已经在使用exe，请跳过此脚本。
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python环境正常
echo.

echo [2/4] 检查playwright模块...
echo ------------------------------------------------------
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ playwright模块未安装
    echo 正在安装playwright模块...
    pip install playwright
    if %errorlevel% neq 0 (
        echo ❌ playwright模块安装失败
        pause
        exit /b 1
    )
)
echo ✅ playwright模块已安装
echo.

echo [3/4] 开始下载并安装Chromium浏览器...
echo ------------------------------------------------------
echo 提示：下载大小约300MB，请耐心等待...
echo.

python -m playwright install chromium --with-deps
set INSTALL_RESULT=%errorlevel%

echo.
if %INSTALL_RESULT% equ 0 (
    echo ✅ Chromium浏览器安装成功！
) else (
    echo ❌ Chromium浏览器安装失败
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题
    echo 2. 磁盘空间不足
    echo 3. 防火墙/杀毒软件拦截
    echo.
    echo 建议：
    echo - 检查网络连接
    echo - 临时关闭杀毒软件
    echo - 稍后重试
    echo.
    pause
    exit /b 1
)

echo.
echo [4/4] 验证安装结果...
echo ------------------------------------------------------

if exist "%LOCALAPPDATA%\ms-playwright\chromium-*" (
    echo ✅ 浏览器文件已创建
    echo 安装位置：
    dir /b "%LOCALAPPDATA%\ms-playwright"
) else (
    echo ⚠️ 浏览器文件未找到
)

echo.
echo ======================================================
echo   安装完成！
echo ======================================================
echo.
echo 现在可以关闭此窗口，重新运行"链接提取工具.exe"
echo.
pause


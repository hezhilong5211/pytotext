@echo off
chcp 65001 >nul
title 打包成exe（单目录版-更稳定）

echo ======================================================
echo   打包成exe（单目录版-包含浏览器）
echo ======================================================
echo.
echo 单目录版优点：
echo   - 打包更稳定，不会因为文件太大失败
echo   - 浏览器文件不需要每次解压
echo   - 启动更快
echo.
echo 缺点：
echo   - 生成一个文件夹，而不是单个exe
echo.
pause

echo.
echo [1/3] 检查本地浏览器...
echo ------------------------------------------------------
python -c "import os; p = os.path.expanduser('~/AppData/Local/ms-playwright'); print(f'浏览器路径: {p}'); print(f'存在: {os.path.exists(p)}')"
echo.

echo [2/3] 开始打包（单目录版）...
echo ------------------------------------------------------
pyinstaller build_exe_onedir.spec --clean --log-level INFO
echo.

echo [3/3] 检查打包结果...
echo ------------------------------------------------------
if exist "dist\链接提取工具" (
    echo ✅ 打包成功！
    echo.
    echo 文件位置: dist\链接提取工具\
    echo.
    dir "dist\链接提取工具" /b
    echo.
    echo 检查浏览器是否包含：
    if exist "dist\链接提取工具\playwright_browsers" (
        echo ✅ 浏览器已包含！
        dir "dist\链接提取工具\playwright_browsers" /b
    ) else (
        echo ❌ 浏览器未包含
    )
) else (
    echo ❌ 打包失败
)

echo.
echo ======================================================
echo   打包完成
echo ======================================================
echo.
echo 使用方法：
echo   1. 将整个 dist\链接提取工具 文件夹拷贝到目标电脑
echo   2. 双击运行 链接提取工具.exe
echo.
pause


@echo off
chcp 65001 >nul
color 0E

echo.
echo ================================================================================
echo                   链接提取工具 - Windows打包脚本
echo ================================================================================
echo.

REM 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo ❌ PyInstaller未安装
    echo 正在安装PyInstaller...
    pip install pyinstaller
    echo.
)

echo [1/4] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✅ 完成

echo.
echo [2/4] 正在打包程序...
echo      这可能需要2-3分钟，请耐心等待...
echo.

pyinstaller --clean build_exe.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ 打包失败！
    echo 请检查错误信息
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成

echo.
echo [3/4] 复制辅助文件到分发目录...

REM 创建分发目录
if not exist "dist\链接提取工具_分发包" mkdir "dist\链接提取工具_分发包"

REM 复制主程序
copy "dist\链接提取工具.exe" "dist\链接提取工具_分发包\" >nul
echo   ✅ 主程序

REM 复制辅助文件
copy "安装Playwright浏览器.bat" "dist\链接提取工具_分发包\" >nul
echo   ✅ 安装脚本

copy "README_首次使用必读.txt" "dist\链接提取工具_分发包\" >nul
echo   ✅ 使用说明

copy "打包和部署指南.md" "dist\链接提取工具_分发包\" >nul
echo   ✅ 部署指南

REM 复制示例文件（如果存在）
if exist "测试数据集_随机抽样.xlsx" (
    copy "测试数据集_随机抽样.xlsx" "dist\链接提取工具_分发包\示例数据.xlsx" >nul
    echo   ✅ 示例数据
)

echo.
echo [4/4] 打包完成统计...
echo.

for %%A in ("dist\链接提取工具.exe") do (
    set size=%%~zA
)
set /a sizeMB=size/1048576
echo   程序大小: %sizeMB% MB
echo   位置: dist\链接提取工具_分发包\
echo.

echo ================================================================================
echo ✅ 打包成功！
echo ================================================================================
echo.
echo 分发包位置:
echo   %CD%\dist\链接提取工具_分发包\
echo.
echo 包含文件:
echo   ✅ 链接提取工具.exe           - 主程序
echo   ✅ 安装Playwright浏览器.bat   - 一键安装脚本
echo   ✅ README_首次使用必读.txt    - 使用说明
echo   ✅ 打包和部署指南.md          - 技术文档
echo   ✅ 示例数据.xlsx              - 示例文件（如果有）
echo.
echo 📝 下一步:
echo   1. 测试 dist\链接提取工具_分发包\链接提取工具.exe
echo   2. 如果测试通过，可以压缩整个文件夹分发
echo   3. 提醒用户首次使用前运行"安装Playwright浏览器.bat"
echo.
echo ================================================================================

pause


#!/bin/bash

echo "======================================================"
echo "本地打包测试脚本"
echo "======================================================"
echo ""

# 检查pyinstaller是否安装
if ! command -v pyinstaller &> /dev/null; then
    echo "❌ PyInstaller未安装，正在安装..."
    pip install pyinstaller
fi

echo "1️⃣ 打包单文件版（带管理员权限）..."
echo "------------------------------------------------------"
pyinstaller build_exe.spec --clean --log-level INFO
if [ $? -eq 0 ]; then
    echo "✅ 单文件版打包成功"
    if [ -f "dist/链接提取工具.exe" ]; then
        mv "dist/链接提取工具.exe" "dist/链接提取工具_单文件版_管理员权限.exe"
        echo "✅ 已重命名为: 链接提取工具_单文件版_管理员权限.exe"
    fi
else
    echo "❌ 单文件版打包失败"
fi

echo ""
echo "2️⃣ 打包单目录版（无需管理员权限）..."
echo "------------------------------------------------------"
pyinstaller build_exe_onedir.spec --clean --log-level INFO
if [ $? -eq 0 ]; then
    echo "✅ 单目录版打包成功"
    if [ -d "dist/链接提取工具" ]; then
        cd dist
        zip -r "链接提取工具_单目录版_无需管理员权限.zip" "链接提取工具"
        cd ..
        echo "✅ 已打包为ZIP: 链接提取工具_单目录版_无需管理员权限.zip"
    fi
else
    echo "❌ 单目录版打包失败"
fi

echo ""
echo "======================================================"
echo "打包完成！"
echo "======================================================"
echo "生成的文件："
ls -lh dist/*.exe dist/*.zip 2>/dev/null

echo ""
echo "注意：本地打包不含Playwright浏览器，需要在Windows上安装："
echo "  python -m playwright install chromium"
echo ""


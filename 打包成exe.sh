#!/bin/bash
# ============================================
# 链接提取工具 - Mac/Linux 打包脚本
# ============================================

echo "========================================"
echo "链接提取工具 - 打包成可执行文件"
echo "========================================"
echo ""

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python"
    exit 1
fi

# 检查依赖
echo "[1/4] 检查依赖..."
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误: 未找到 tkinter"
    echo "在 Mac 上，tkinter 应该已经包含在 Python 中"
    echo "在 Linux 上，请运行: sudo apt-get install python3-tk"
    exit 1
fi
echo "依赖检查通过"
echo ""

# 安装/更新打包依赖
echo "[2/4] 安装/更新依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi
echo ""

# 安装 Playwright 浏览器（可选）
echo "[3/4] 安装 Playwright 浏览器（用于百度/抖音）..."
python3 -m playwright install chromium
if [ $? -ne 0 ]; then
    echo "警告: Playwright 安装失败，部分功能可能受限"
fi
echo ""

# 打包
echo "[4/4] 开始打包..."
pyinstaller build_exe.spec --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "打包成功！"
    echo "========================================"
    echo ""
    echo "可执行文件位置: dist/链接提取工具"
    echo ""
    echo "您可以将 dist 文件夹中的所有内容复制到其他电脑使用"
    echo ""
else
    echo ""
    echo "========================================"
    echo "打包失败！"
    echo "========================================"
    echo ""
    echo "请检查错误信息"
    exit 1
fi


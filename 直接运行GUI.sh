#!/bin/bash
# ============================================
# 快速启动 - Mac/Linux
# ============================================

echo "正在启动链接提取工具..."
python3 链接提取工具_GUI版.py

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败，请确保已安装所需依赖："
    echo "pip3 install -r requirements.txt"
fi


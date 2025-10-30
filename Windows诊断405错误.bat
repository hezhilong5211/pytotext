@echo off
chcp 65001 >nul
title Windows 405错误诊断

echo ======================================================
echo   Windows 405错误诊断脚本
echo ======================================================
echo.

echo [1/5] 检查Python环境...
echo ------------------------------------------------------
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    pause
    exit /b 1
)
echo.

echo [2/5] 检查requests库版本...
echo ------------------------------------------------------
pip show requests
echo.

echo [3/5] 测试基础HTTP连接...
echo ------------------------------------------------------
python -c "import requests; r = requests.get('https://www.baidu.com'); print(f'百度: {r.status_code}')"
python -c "import requests; r = requests.get('https://www.google.com'); print(f'谷歌: {r.status_code}')"
echo.

echo [4/5] 测试汽车之家连接...
echo ------------------------------------------------------
python -c "import requests; headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}; r = requests.get('https://www.autohome.com.cn', headers=headers, timeout=10); print(f'汽车之家: {r.status_code}')"
echo.

echo [5/5] 测试小红书连接...
echo ------------------------------------------------------
python -c "import requests; headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}; r = requests.get('https://www.xiaohongshu.com', headers=headers, timeout=10); print(f'小红书: {r.status_code}')"
echo.

echo ======================================================
echo   诊断完成
echo ======================================================
echo.
echo 请截图上述输出并发送给开发者。
echo.
pause


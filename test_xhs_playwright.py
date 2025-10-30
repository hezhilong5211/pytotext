#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用Playwright测试小红书explore链接"""

from playwright.sync_api import sync_playwright
import re
import time

url = "https://www.xiaohongshu.com/explore/6901954c0000000004001a1c"

print("=" * 60)
print("使用Playwright访问小红书explore链接")
print("=" * 60)
print(f"URL: {url}")
print()

try:
    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)  # 改为可见模式调试
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        print("正在访问URL...")
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        print(f"当前URL: {page.url}")
        
        # 检查是否被重定向
        if '/404' in page.url or 'error_code' in page.url:
            print("❌ 被重定向到错误页面")
        else:
            print("✅ 没有异常重定向")
        
        print("等待5秒让页面完全加载...")
        time.sleep(5)
        
        html_content = page.content()
        print(f"HTML长度: {len(html_content)} 字符")
        
        # 保存HTML
        with open('xhs_playwright.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✅ HTML已保存到: xhs_playwright.html")
        
        # 查找JSON数据
        patterns = [
            (r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>', '__INITIAL_STATE__'),
            (r'window\.__SETUP_SERVER_STATE__\s*=\s*({.+?})\s*<\/script>', '__SETUP_SERVER_STATE__'),
        ]
        
        for pattern, name in patterns:
            matches = re.findall(pattern, html_content, re.DOTALL)
            if matches:
                json_str = matches[0]
                print(f"\n✅ 找到 {name}，长度: {len(json_str)}")
                
                # 提取字段
                desc_match = re.search(r'"desc"\s*:\s*"([^"]+)"', json_str)
                title_match = re.search(r'"title"\s*:\s*"([^"]+)"', json_str)
                nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
                
                if desc_match:
                    print(f"  描述: {desc_match.group(1)[:100]}")
                if title_match:
                    print(f"  标题: {title_match.group(1)[:100]}")
                if nick_match:
                    print(f"  作者: {nick_match.group(1)}")
        
        print("\n等待10秒查看页面（headless=False模式）...")
        time.sleep(10)
        
        browser.close()
        print("浏览器已关闭")
        
except Exception as e:
    print(f"❌ 错误: {e}")


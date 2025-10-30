#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试使用Firefox绕过小红书反爬虫"""

from playwright.sync_api import sync_playwright
import re
import time

url = "https://www.xiaohongshu.com/explore/6901954c0000000004001a1c"

print("=" * 60)
print("测试方法: 使用Firefox浏览器")
print("=" * 60)
print("（Firefox的自动化特征与Chrome不同）")
print()

try:
    with sync_playwright() as p:
        # 使用Firefox而不是Chromium
        browser = p.firefox.launch(
            headless=True,
            firefox_user_prefs={
                "dom.webdriver.enabled": False,  # 禁用webdriver标志
                "useAutomationExtension": False,
                "general.platform.override": "Win64",
            }
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            locale='zh-CN',
        )
        
        page = context.new_page()
        
        print("正在访问URL...")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)
        
        current_url = page.url
        print(f"当前URL: {current_url[:100]}...")
        
        if '/404' in current_url or 'captcha' in current_url or 'error_code' in current_url:
            print("❌ Firefox方法失败：仍被重定向")
        else:
            print("✅✅✅ Firefox方法成功：没有重定向！！！")
            
            html_content = page.content()
            
            # 保存HTML
            with open('xhs_firefox_success.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✅ HTML已保存")
            
            # 查找数据
            pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if matches:
                json_str = matches[0]
                
                desc_match = re.search(r'"desc"\s*:\s*"([^"]{10,})"', json_str)
                title_match = re.search(r'"title"\s*:\s*"([^"]{5,})"', json_str)
                nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
                
                print()
                print("提取结果：")
                if desc_match:
                    print(f"  描述: {desc_match.group(1)[:80]}")
                if title_match:
                    print(f"  标题: {title_match.group(1)[:80]}")
                if nick_match:
                    print(f"  作者: {nick_match.group(1)}")
                    
                if (desc_match or title_match) and nick_match:
                    print()
                    print("🎉🎉🎉 完全成功！Firefox可以绕过反爬虫！")
            else:
                print("⚠️ 没有找到JSON数据")
        
        browser.close()
        
except Exception as e:
    print(f"❌ Firefox异常: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 60)


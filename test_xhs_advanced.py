#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试高级方法绕过小红书反爬虫"""

from playwright.sync_api import sync_playwright
import re
import time

url = "https://www.xiaohongshu.com/explore/6901954c0000000004001a1c"

print("=" * 60)
print("测试方法1: Playwright隐藏自动化特征")
print("=" * 60)

try:
    with sync_playwright() as p:
        # 启动浏览器（禁用自动化特征）
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',  # 禁用自动化控制特征
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        
        # 创建上下文，设置更真实的环境
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
        )
        
        page = context.new_page()
        
        # 注入脚本隐藏webdriver特征
        page.add_init_script("""
            // 覆盖navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // 覆盖permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // 添加chrome对象
            window.chrome = {
                runtime: {}
            };
            
            // 伪装plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // 伪装languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en']
            });
        """)
        
        print("正在访问URL...")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # 等待并检查
        time.sleep(5)
        
        current_url = page.url
        print(f"当前URL: {current_url[:100]}...")
        
        if '/404' in current_url or 'captcha' in current_url or 'error_code' in current_url:
            print("❌ 方法1失败：仍被重定向")
        else:
            print("✅ 方法1成功：没有重定向！")
            
            html_content = page.content()
            
            # 查找数据
            pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if matches:
                json_str = matches[0]
                desc_match = re.search(r'"desc"\s*:\s*"([^"]{10,})"', json_str)
                nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
                
                if desc_match and nick_match:
                    print(f"✅✅ 提取成功！")
                    print(f"  标题: {desc_match.group(1)[:50]}")
                    print(f"  作者: {nick_match.group(1)}")
        
        browser.close()
        
except Exception as e:
    print(f"❌ 方法1异常: {e}")

print()
print("=" * 60)
print("测试方法2: 使用持久化上下文（模拟真实浏览器）")
print("=" * 60)

try:
    import tempfile
    import os
    
    with sync_playwright() as p:
        # 使用持久化上下文（会保存cookies等）
        user_data_dir = tempfile.mkdtemp()
        
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
            ],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-CN',
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        # 隐藏webdriver
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        print("正在访问URL...")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)
        
        current_url = page.url
        print(f"当前URL: {current_url[:100]}...")
        
        if '/404' in current_url or 'captcha' in current_url or 'error_code' in current_url:
            print("❌ 方法2失败：仍被重定向")
        else:
            print("✅ 方法2成功：没有重定向！")
            
            html_content = page.content()
            pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if matches:
                json_str = matches[0]
                desc_match = re.search(r'"desc"\s*:\s*"([^"]{10,})"', json_str)
                nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
                
                if desc_match and nick_match:
                    print(f"✅✅ 提取成功！")
                    print(f"  标题: {desc_match.group(1)[:50]}")
                    print(f"  作者: {nick_match.group(1)}")
        
        context.close()
        
        # 清理临时目录
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)
        
except Exception as e:
    print(f"❌ 方法2异常: {e}")

print()
print("=" * 60)
print("测试方法3: 先访问首页再访问目标页")
print("=" * 60)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
        )
        
        page = context.new_page()
        
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # 先访问首页建立session
        print("先访问小红书首页...")
        page.goto('https://www.xiaohongshu.com/', wait_until='domcontentloaded')
        time.sleep(2)
        
        # 再访问目标页
        print("再访问目标页...")
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        time.sleep(5)
        
        current_url = page.url
        print(f"当前URL: {current_url[:100]}...")
        
        if '/404' in current_url or 'captcha' in current_url or 'error_code' in current_url:
            print("❌ 方法3失败：仍被重定向")
        else:
            print("✅ 方法3成功：没有重定向！")
            
            html_content = page.content()
            pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>'
            matches = re.findall(pattern, html_content, re.DOTALL)
            
            if matches:
                json_str = matches[0]
                desc_match = re.search(r'"desc"\s*:\s*"([^"]{10,})"', json_str)
                nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
                
                if desc_match and nick_match:
                    print(f"✅✅ 提取成功！")
                    print(f"  标题: {desc_match.group(1)[:50]}")
                    print(f"  作者: {nick_match.group(1)}")
        
        browser.close()
        
except Exception as e:
    print(f"❌ 方法3异常: {e}")

print()
print("=" * 60)
print("总结")
print("=" * 60)
print("如果所有方法都失败，说明小红书的反爬虫确实很严格")
print("建议：使用xhslink.com短链接")


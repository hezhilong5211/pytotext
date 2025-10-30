#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Windows 405错误详细诊断"""

import requests
import sys

def test_url(url, description):
    """测试单个URL"""
    print(f"\n{'='*60}")
    print(f"测试: {description}")
    print(f"URL: {url}")
    print('-'*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        print(f"✅ 状态码: {response.status_code}")
        print(f"最终URL: {response.url[:100]}...")
        print(f"响应大小: {len(response.content)} 字节")
        
        # 显示响应头
        print("\n响应头（部分）:")
        for key in ['Content-Type', 'Server', 'Set-Cookie']:
            if key in response.headers:
                print(f"  {key}: {response.headers[key][:100]}")
        
        if response.status_code == 405:
            print("\n❌ 405错误详情:")
            print(f"  允许的方法: {response.headers.get('Allow', '未指定')}")
            print(f"  响应内容（前500字符）:")
            print(f"  {response.text[:500]}")
        elif response.status_code >= 400:
            print(f"\n❌ 错误 {response.status_code}")
            print(f"  响应内容（前500字符）:")
            print(f"  {response.text[:500]}")
        else:
            print(f"✅ 请求成功")
            
    except Exception as e:
        print(f"❌ 异常: {e}")

# 测试环境信息
print("="*60)
print("Python环境信息")
print("="*60)
print(f"Python版本: {sys.version}")
print(f"requests版本: {requests.__version__}")
print()

# 测试各个网站
test_url('https://www.baidu.com', '百度首页（基础测试）')
test_url('https://www.autohome.com.cn', '汽车之家首页')
test_url('https://chejiahao.autohome.com.cn/info/22979065', '汽车之家车家号文章')
test_url('http://xhslink.com/o/6xxLJMbzsSA', '小红书短链接')
test_url('https://www.xiaohongshu.com', '小红书首页')

print("\n" + "="*60)
print("诊断完成")
print("="*60)
print("\n如果看到405错误，请截图发送给开发者。")
print("特别注意：")
print("  - 哪些网站返回405")
print("  - 响应头中的'Allow'字段")
print("  - 错误详情内容")


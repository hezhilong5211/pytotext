#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试能访问的小红书链接"""

import requests
import re

url = "https://www.xiaohongshu.com/explore/6901954c0000000004001a1c?app_platform=android&ignoreEngage=true&app_version=9.3.0&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBqObC79XFiNUXvk55J8kEKiudZE4R-9jnNbBCNj6rXAE=&author_share=1&xhsshare=WeixinSession&shareRedId=ODdGMzM4Ozo2NzUyOTgwNjczOTdHPD1N&apptime=1761712811&share_id=973e7cf7dda94026b62ab4de8eef7f6b&share_channel=wechat"

# 提取ID并清理
note_id = re.search(r'/explore/([0-9a-f]+)', url).group(1)
clean_url = f'https://www.xiaohongshu.com/explore/{note_id}'

print(f"原URL: {url[:80]}...")
print(f"笔记ID: {note_id}")
print(f"清理后URL: {clean_url}")
print()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.xiaohongshu.com/',
}

print("正在请求...")
response = requests.get(clean_url, headers=headers, timeout=15, allow_redirects=True)

print(f"状态码: {response.status_code}")
print(f"最终URL: {response.url}")
print(f"内容长度: {len(response.text)} 字符")
print()

# 检查重定向
if '/404' in response.url:
    print("❌ 被重定向到404")
elif 'weixin.qq.com' in response.url:
    print("❌ 被重定向到微信")
elif 'website-login' in response.url:
    print("❌ 被重定向到登录页")
elif 'error_code' in response.url:
    print("❌ URL包含error_code")
else:
    print("✅ 没有异常重定向")

# 查找JSON
patterns = [
    (r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*<\/script>', '__INITIAL_STATE__'),
    (r'window\.__SETUP_SERVER_STATE__\s*=\s*({.+?})\s*<\/script>', '__SETUP_SERVER_STATE__'),
]

for pattern, name in patterns:
    matches = re.findall(pattern, response.text, re.DOTALL)
    if matches:
        json_str = matches[0]
        print(f"\n✅ 找到 {name}，长度: {len(json_str)} 字符")
        
        # 提取关键字段
        title_match = re.search(r'"title"\s*:\s*"([^"]{5,})"', json_str)
        desc_match = re.search(r'"desc"\s*:\s*"([^"]{10,})"', json_str)
        nick_match = re.search(r'"nickName"\s*:\s*"([^"]{2,30})"', json_str)
        
        if title_match:
            print(f"  标题 (title): {title_match.group(1)[:100]}")
        if desc_match:
            print(f"  描述 (desc): {desc_match.group(1)[:100]}")
        if nick_match:
            print(f"  作者 (nickName): {nick_match.group(1)}")
        
        if not (title_match or desc_match or nick_match):
            print("  ⚠️ 未找到title/desc/nickName字段")
            # 显示JSON前500字符
            print(f"  JSON预览: {json_str[:500]}")

# 保存HTML
with open('xhs_working.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
print(f"\n✅ HTML已保存到: xhs_working.html")


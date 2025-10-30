#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试汽车之家链接提取"""

from extract_links_v4_final import extract_autohome_info
import json

url = "https://chejiahao.autohome.com.cn/info/22979065"

print("=" * 60)
print("测试汽车之家链接提取")
print("=" * 60)
print(f"URL: {url}")
print()

result = extract_autohome_info(url)

print("提取结果：")
print(json.dumps(result, ensure_ascii=False, indent=2))
print()
print("=" * 60)

if result['title'] and result['title'] != '未找到标题':
    print(f"✅ 标题: {result['title']}")
else:
    print(f"❌ 标题: {result['title']}")

if result['author'] and result['author'] != '未找到作者':
    print(f"✅ 作者: {result['author']}")
else:
    print(f"❌ 作者: {result['author']}")

print(f"状态: {result['status']}")
print()

# 预期结果（从网页内容）
print("预期结果：")
print("标题: 岚图追光L静态体验")
print("作者: 张抗抗")


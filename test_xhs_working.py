#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试能正常访问的小红书链接"""

from extract_links_v4_final import extract_xiaohongshu_info
import json

url = "https://www.xiaohongshu.com/explore/6901954c0000000004001a1c?app_platform=android&ignoreEngage=true&app_version=9.3.0&share_from_user_hidden=true&xsec_source=app_share&type=normal&xsec_token=CBqObC79XFiNUXvk55J8kEKiudZE4R-9jnNbBCNj6rXAE=&author_share=1&xhsshare=WeixinSession&shareRedId=ODdGMzM4Ozo2NzUyOTgwNjczOTdHPD1N&apptime=1761712811&share_id=973e7cf7dda94026b62ab4de8eef7f6b&share_channel=wechat"

print("=" * 60)
print("测试小红书链接提取")
print("=" * 60)
print(f"URL: {url[:80]}...")
print()

result = extract_xiaohongshu_info(url)

print("提取结果：")
print(json.dumps(result, ensure_ascii=False, indent=2))
print()
print("=" * 60)

if result['title'] and result['title'] != '未找到标题' and '访问受限' not in result['title']:
    print(f"✅ 标题: {result['title']}")
else:
    print(f"❌ 标题: {result['title']}")

if result['author'] and result['author'] != '未找到作者' and '访问受限' not in result['author']:
    print(f"✅ 作者: {result['author']}")
else:
    print(f"❌ 作者: {result['author']}")

print(f"状态: {result['status']}")
print()

# 预期结果（从网页内容）
print("预期结果：")
print("标题: TA俩同框也太养眼了吧！")
print("作者: 高段位拆机")


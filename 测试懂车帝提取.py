"""
懂车帝链接测试脚本 - 直接运行查看调试信息
"""
import sys
import os
from datetime import datetime

# 确保能导入主模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("懂车帝链接测试工具")
print("=" * 60)
print()

# 测试链接
test_urls = [
    "https://dcd.zjbyte.cn/i7556920965762990646/",
    "https://dcd.zjbyte.cn/i7556911855051063818/",
]

print("导入提取模块...")
try:
    from extract_links_v4_final import extract_dongchedi_info, PLAYWRIGHT_AVAILABLE
    print(f"✅ 模块导入成功")
    print(f"   Playwright可用: {'是' if PLAYWRIGHT_AVAILABLE else '否'}")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    input("\n按回车键退出...")
    sys.exit(1)

print()
print("=" * 60)
print("开始测试")
print("=" * 60)
print()

for i, url in enumerate(test_urls, 1):
    print(f"\n[测试 {i}/{len(test_urls)}]")
    print(f"链接: {url}")
    print("-" * 60)
    
    try:
        result = extract_dongchedi_info(url)
        
        print(f"\n结果:")
        print(f"  标题: {result.get('title', '未知')}")
        print(f"  作者: {result.get('author', '未知')}")
        print(f"  状态: {result.get('status', '未知')}")
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 60)
print("测试完成")
print("=" * 60)
print()

# 检查调试文件
debug_files = ['dongchedi_debug.log', 'dongchedi_page.html']
print("查找调试文件:")
for filename in debug_files:
    if os.path.exists(filename):
        abs_path = os.path.abspath(filename)
        file_size = os.path.getsize(filename)
        print(f"  ✅ {filename}")
        print(f"     位置: {abs_path}")
        print(f"     大小: {file_size:,} 字节")
    else:
        print(f"  ❌ {filename} - 未找到")

print()
input("按回车键退出...")


# 抖音Token/Cookie配置说明

## 功能说明

如果您有抖音账号的Cookie或Token，可以在代码中配置后使用，这样可以：
- ✅ 提高提取成功率
- ✅ 访问需要登录的视频链接
- ✅ 避免验证码拦截
- ✅ 获取更完整的数据

## 如何获取抖音Cookie

### 方法1：从浏览器开发者工具获取（推荐）

1. **打开浏览器**，访问 https://www.douyin.com/
2. **登录你的抖音账号**
3. **按F12** 打开开发者工具
4. **切换到Application标签页**（Chrome）或**存储标签页**（Firefox）
5. **左侧找到Cookies** → 展开 → 点击 `https://www.douyin.com`
6. **复制所有Cookie值**：
   - Chrome: 右键 → Copy → Copy all as cURL
   - 或者手动复制关键Cookie，格式：`sessionid=xxx; sid_guard=xxx; ...`

### 方法2：从Network请求中获取

1. **打开浏览器开发者工具**（F12）
2. **切换到Network标签页**
3. **刷新页面**或访问任意抖音视频
4. **找到任意请求**（如 `video` 或页面请求）
5. **点击请求** → 查看 **Request Headers**
6. **复制Cookie行的值**

### 方法3：从浏览器插件获取

使用Cookie导出插件（如EditThisCookie）可以直接导出Cookie字符串

## 配置方法

在 `extract_links_v4_final.py` 文件中找到：

```python
DOUYIN_COOKIE = ''  # 留空表示不使用Cookie，填写后会自动使用
```

将Cookie字符串填入，例如：

```python
DOUYIN_COOKIE = 'sessionid=abc123; sid_guard=def456; ttwid=ghi789; ...'
```

**注意**：
- Cookie字符串中的每个键值对用 `; `（分号+空格）分隔
- 不需要包含 `Cookie:` 前缀
- 保留所有必要的Cookie，特别是 `sessionid`、`sid_guard` 等

## 重要Cookie说明

抖音的关键Cookie通常包括：

- **sessionid**: 会话ID（最重要）
- **sid_guard**: 会话保护
- **ttwid**: 设备ID
- **msToken**: 反爬虫token
- **odin_tt**: 用户标识

## 测试配置

配置完成后，可以测试是否生效：

```python
python3 -c "
from extract_links_v4_final import extract_douyin_enhanced
result = extract_douyin_enhanced('https://v.douyin.com/xxx/')
print(result)
"
```

如果之前失败的链接现在能成功提取，说明配置生效。

## 安全提示

⚠️ **重要**：
- Cookie包含登录凭证，请妥善保管，不要泄露
- 不要将包含Cookie的代码提交到公开仓库
- Cookie可能会过期，需要定期更新
- 建议使用专用账号的Cookie，不要使用主账号

## 常见问题

**Q: Cookie多久过期？**
A: 通常是几天到几周，具体取决于抖音的策略。过期后需要重新获取。

**Q: 一个Cookie可以访问所有视频吗？**
A: 大部分公开视频可以，但某些私有视频或需要特定权限的内容可能需要其他认证。

**Q: 配置Cookie后还是失败怎么办？**
A: 
1. 检查Cookie格式是否正确
2. 确认Cookie未过期
3. 尝试重新登录获取新的Cookie
4. 检查视频链接是否真的需要登录（某些链接可能本身就无法访问）

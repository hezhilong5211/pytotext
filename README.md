# 🔗 链接标题和作者提取工具

一个功能强大的链接信息提取工具，支持从Excel中提取链接并自动获取标题和作者信息。

## ✨ 主要特性

### 🎯 核心功能
- ✅ **文件上传**: 支持Excel文件（.xlsx, .xls）导入
- 📊 **实时进度**: 可视化进度条和百分比显示
- 📋 **日志显示**: 实时彩色日志输出，清晰追踪处理状态
- 💾 **结果导出**: Excel格式导出，支持颜色标记
- 🎨 **颜色标记**: 
  - 🔴 404错误 → 整行标红
  - 🟡 提取失败 → 单元格标黄

### 🌐 支持平台
- **哔哩哔哩** (Bilibili) - 98%+ 成功率
- **微博** (Weibo) - 98%+ 成功率  
- **小红书** (Xiaohongshu) - 90%+ 成功率
- **抖音** (Douyin) - 80%+ 成功率（两阶段处理）
- **今日头条** (Toutiao) - 80%+ 成功率
- **汽车之家** (Autohome) - 90%+ 成功率
- **百家号/百度系** - 66%+ 成功率（两阶段处理）
- **懂车帝** (Dongchedi)
- **知乎** (Zhihu)
- **买车网** (Maiche)
- 以及其他通用网站

### 🚀 两阶段处理策略
1. **阶段1**: 快速处理普通链接（跳过百度/抖音）
2. **阶段2**: 使用Playwright浏览器处理难处理的百度系和抖音链接

## 📦 安装说明

### 方式1: 使用源码（推荐开发）

#### 1. 安装依赖
```bash
# Windows
pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

#### 2. 安装Playwright浏览器（可选，但强烈推荐）
```bash
# Windows
python -m playwright install chromium

# Mac/Linux
python3 -m playwright install chromium
```

#### 3. 运行程序

**GUI版本（推荐）:**
```bash
# Windows - 双击运行
直接运行GUI.bat

# 或使用命令行
python 链接提取工具_GUI版.py

# Mac/Linux
bash 直接运行GUI.sh

# 或使用命令行
python3 链接提取工具_GUI版.py
```

**命令行版本:**
```bash
# Windows
python extract_links_v4_final.py

# Mac/Linux
python3 extract_links_v4_final.py
```

### 方式2: 打包成EXE（推荐分发）

#### Windows 打包
```bash
# 双击运行打包脚本
打包成exe.bat

# 或使用命令行
pyinstaller build_exe.spec --clean
```

#### Mac/Linux 打包
```bash
# 添加执行权限并运行
chmod +x 打包成exe.sh
./打包成exe.sh

# 或使用命令行
pyinstaller build_exe.spec --clean
```

打包完成后，可执行文件在 `dist` 文件夹中：
- Windows: `dist\链接提取工具.exe`
- Mac/Linux: `dist/链接提取工具`

## 🎮 使用指南

### GUI版本使用步骤

1. **启动程序**
   - Windows: 双击 `链接提取工具.exe` 或 `直接运行GUI.bat`
   - Mac/Linux: 运行 `./直接运行GUI.sh`

2. **选择输入文件**
   - 点击"浏览"按钮
   - 选择包含链接的Excel文件
   - 程序会自动设置输出文件名

3. **开始处理**
   - 点击"▶️ 开始处理"按钮
   - 实时查看日志和进度
   - 可随时点击"⏹️ 停止"中断处理

4. **查看结果**
   - 处理完成后会显示统计信息
   - 结果自动保存到输出文件
   - 可点击"💾 导出结果"另存到其他位置

### 命令行版本使用

编辑 `extract_links_v4_final.py` 第871行，修改输入文件：
```python
excel_file = '你的文件名.xlsx'
```

然后运行：
```bash
python extract_links_v4_final.py
```

## 📊 输出格式

生成的Excel文件包含以下列：
- **原链接**: 原始URL
- **网站名**: 识别的平台名称
- **作者**: 提取的作者信息
- **标题**: 提取的标题信息
- **状态**: 处理状态（success/partial/failed）

### 颜色标记
- 🔴 **整行红色**: 404错误或链接失效
- 🟡 **单元格黄色**: 标题或作者提取失败

## 🔧 技术架构

### 核心技术栈
- **Python 3.8+**: 主要开发语言
- **Tkinter**: GUI界面框架
- **Pandas**: 数据处理
- **Requests**: HTTP请求
- **BeautifulSoup4**: HTML解析
- **Playwright**: 浏览器自动化（处理动态内容）
- **OpenPyXL**: Excel文件操作

### 提取策略
1. **API提取**: 微博、B站等使用官方/移动端API
2. **HTML解析**: 静态网页使用BeautifulSoup解析
3. **JSON提取**: 从页面JavaScript数据中提取
4. **浏览器渲染**: 百度系和抖音使用Playwright渲染

## 📝 依赖列表

```txt
# 核心依赖
pandas>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
openpyxl>=3.1.0

# Playwright（可选，用于百度/抖音/今日头条）
playwright>=1.40.0

# 打包工具
pyinstaller>=6.0.0
```

## ❓ 常见问题

### Q1: 为什么百度系和抖音成功率较低？
**A**: 这些平台有较强的反爬虫机制。程序采用两阶段处理策略，第二阶段使用Playwright浏览器可以提高成功率。

### Q2: Playwright安装失败怎么办？
**A**: 
- 确保网络连接正常
- 尝试手动安装：`python -m playwright install chromium`
- 如果仍然失败，程序会降级使用requests（效果会打折扣）

### Q3: 打包的EXE文件很大？
**A**: 这是正常的，因为包含了Python运行时和所有依赖库。可以：
- 压缩成zip分发
- 使用UPX压缩（已在spec文件中启用）

### Q4: Mac上提示"无法打开，因为无法验证开发者"？
**A**: 
```bash
# 右键点击应用，选择"打开"
# 或在终端运行：
xattr -cr dist/链接提取工具.app
```

### Q5: 处理速度慢？
**A**: 
- 阶段1（普通链接）：约0.5-2秒/个
- 阶段2（百度/抖音）：约3-8秒/个
- 这是为了避免触发反爬虫机制
- 可以在代码中调整延迟时间

## 🐛 故障排除

### 程序无法启动
```bash
# 检查Python版本（需要3.8+）
python --version

# 重新安装依赖
pip install -r requirements.txt --upgrade
```

### 导入错误
```bash
# 确保在正确的目录
cd /path/to/pytiqutitle

# 检查文件是否存在
ls -la
```

### GUI界面显示异常
- **Windows**: 确保安装了完整的Python（不是Microsoft Store版本）
- **Linux**: 安装tk支持：`sudo apt-get install python3-tk`
- **Mac**: tkinter应该已包含在Python中

## 📄 文件说明

```
pytiqutitle/
├── 链接提取工具_GUI版.py      # GUI版本主程序 ⭐
├── extract_links_v4_final.py  # 命令行版本主程序
├── requirements.txt           # 依赖列表
├── build_exe.spec            # PyInstaller配置文件
├── 打包成exe.bat             # Windows打包脚本
├── 打包成exe.sh              # Mac/Linux打包脚本
├── 直接运行GUI.bat           # Windows快速启动
├── 直接运行GUI.sh            # Mac/Linux快速启动
├── README.md                 # 本文档
├── 测试数据集_随机抽样.xlsx   # 测试数据
└── dist/                     # 打包输出目录
```

## 📈 性能指标

- **处理速度**: 平均2-5秒/链接
- **内存占用**: 约100-300MB
- **支持规模**: 测试支持1000+链接
- **成功率**: 整体85%+

## 🔒 隐私说明

- ✅ 本工具完全本地运行，不上传任何数据
- ✅ 所有网络请求仅用于访问目标网站
- ✅ 不收集用户信息

## 📜 许可证

本项目仅供学习和研究使用。使用本工具时请遵守目标网站的服务条款和robots.txt规则。

## 🤝 技术支持

如有问题，请检查：
1. Python版本是否>=3.8
2. 依赖是否正确安装
3. 输入文件格式是否正确
4. 网络连接是否正常

## 📌 版本历史

### v4.6 (2024-10-29)
- ✅ 新增GUI版本
- ✅ 实现两阶段处理策略
- ✅ 优化百度系和抖音处理
- ✅ 添加实时日志显示
- ✅ 支持打包成EXE

### v4.5
- ✅ 精准颜色标记
- ✅ Playwright自动化
- ✅ 微博突破98%

### v4.0
- ✅ 多平台支持
- ✅ 批量处理
- ✅ Excel导入导出

---

**享受使用！如有建议欢迎反馈。** 🎉


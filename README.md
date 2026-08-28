# 电脑推荐助手 🤖

基于 **FastAPI + LLM + 联网搜索** 的智能电脑推荐对话机器人。通过自然对话了解用户需求，结合实时搜索数据，为不同人群推荐合适的笔记本和台式机。

## 功能特点

- **💬 对话式交互**：像聊天一样说出需求，AI 自动理解
- **🔍 联网搜索**：通过 Tavily API 获取最新产品价格和评测
- **📊 可视化展示**：价格排序表格、评分雷达图、产品对比卡片
- **🎯 精准匹配**：根据预算/用途/人群多维评分排序
- **🖥️ 全面覆盖**：笔记本 + 台式机智能分类推荐

## 核心交互逻辑

```
用户输入 → LLM 意图分析
   ├─ 提到"笔记本" → 推荐笔记本
   ├─ 提到"台式机" → 推荐台式机
   ├─ 两者都提到  → 两类都推荐
   └─ 未明确      → 反问用户 → 说"不知道"→ 两类都推荐

→ 提取预算/用途 → 联网搜索 → 多维评分 → 可视化推荐
```

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

复制 `.env.example` 为 `.env`，再填入密钥：

```env
# LLM API (支持 DeepSeek / OpenAI / Qwen)
LLM_API_KEY=sk-your-api-key-here
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat

# 搜索 API (可选，无搜索则使用内置演示数据)
TAVILY_API_KEY=tvly-your-tavily-key-here
```

### 3. 启动服务

```bash
python run.py
```

浏览器访问 `http://127.0.0.1:8000`

## 项目结构

```
网络评测笔记本电脑/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── api/                 # API 端点
│   │   ├── chat.py          # WebSocket 聊天
│   │   └── health.py        # 健康检查
│   ├── core/                # 对话核心
│   │   ├── chat_manager.py  # 对话状态机
│   │   ├── conversation.py  # 状态定义
│   │   └── session_store.py # 会话存储
│   ├── llm/                 # LLM 交互
│   │   ├── client.py        # API 客户端
│   │   ├── prompts.py       # 提示词模板
│   │   └── parsers.py       # 结果解析
│   ├── search/              # 搜索模块
│   │   ├── engine.py        # 搜索接口
│   │   ├── tavily_engine.py # Tavily 实现
│   │   ├── query_builder.py # 查询生成
│   │   └── cache.py         # 搜索缓存
│   ├── recommend/           # 推荐引擎
│   ├── models/              # 数据模型
│   ├── db/                  # 数据库
│   └── visualization/       # 可视化数据
├── static/
│   ├── css/                 # 样式文件
│   └── js/                  # 前端脚本
├── templates/
│   └── index.html           # 主页面
├── requirements.txt
├── .env.example             # 配置模板（不含真实密钥）
└── run.py                   # 启动脚本
```

## 技术栈

| 组件 | 选型 |
|------|------|
| Web 框架 | FastAPI |
| 实时通信 | WebSocket |
| 前端 | 纯 HTML/CSS/JS + Chart.js |
| LLM | DeepSeek / OpenAI / Qwen |
| 搜索 | Tavily API |
| 数据库 | SQLite + SQLAlchemy |

## 部署参赛建议

### 本地演示
```bash
python run.py
# 浏览器打开 http://localhost:8000
```

### 云部署 (Railway / Render)
1. 上传项目到 GitHub
2. 在 Railway 中连接仓库
3. 设置环境变量 `LLM_API_KEY` 和 `TAVILY_API_KEY`
4. 启动命令: `python run.py`

## 现有风险与后续优化

> 本项目仅使用合成/演示数据作为公开 Demo。不要提交真实 API Key、Cookie、服务器信息、用户数据或平台账号配置。

- **数据源**: 无搜索 API 时使用内置演示数据，效果有限
- **搜索质量**: 搜索结果取决于 Tavily 覆盖面和 LLM 解析能力
- **价格时效**: 电子产品价格波动快，实时搜索可解决此问题
- **后续优化**:
  - 增加京东/淘宝爬虫作为搜索补充
  - 支持多轮对话追问历史
  - 增加产品型号数据库做离线缓存
  - 加入用户评分反馈机制


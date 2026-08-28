# 电脑推荐助手 - 架构文档

## 一、系统概述

**电脑推荐助手** 是一个基于 FastAPI + LLM + 联网搜索的智能对话机器人。用户通过自然语言描述需求，系统进行意图分析、联网搜索、多源评测聚合评分，最终以可视化方式推荐合适的笔记本和台式机。

### 核心能力

- 💬 **自然语言对话**：理解用户对电脑的需求描述
- 🔍 **多源数据聚合**：整合视频评测、图文评测、论坛讨论等多源评价
- 📊 **透明评分体系**：每项评分来源可追溯，用户可查看评分明细
- 🎯 **精准匹配**：基于预算、用途、品牌偏好等多维度匹配

---

## 二、整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端层 (Browser)                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  templates/index.html  (SPA 主页面)                        │  │
│  │  static/css/*.css      (样式)                              │  │
│  │  static/js/app.js      (WebSocket 连接 + 消息收发)          │  │
│  │  static/js/chat.js     (消息渲染 + 图表 + 评分明细)          │  │
│  │  static/js/utils.js    (工具函数)                           │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │ WebSocket (ws://host:port/ws/chat)    │
├─────────────────────────┼───────────────────────────────────────┤
│                     API 层 (FastAPI)                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  app/main.py          入口 + 路由注册                      │  │
│  │  app/api/chat.py      WebSocket 聊天端点                    │  │
│  │  app/api/health.py    健康检查接口                          │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │                                       │
├─────────────────────────┼───────────────────────────────────────┤
│                    核心业务层                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  app/core/chat_manager.py   对话状态机 (核心编排)           │  │
│  │  app/core/conversation.py   会话状态定义                   │  │
│  │  app/core/session_store.py  会话存储 (内存 dict)           │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  app/llm/client.py          LLM API 客户端封装             │  │
│  │  app/llm/prompts.py         提示词模板                    │  │
│  │  app/llm/parsers.py         LLM 输出解析 (三重容错)        │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  app/recommend/aggregator.py  多源聚合评分引擎             │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  app/search/tavily_engine.py   联网搜索实现                │  │
│  │  app/search/cache.py          搜索缓存 (LRU)              │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │  app/data_collector/          数据采集模块                 │  │
│  │  app/data_collector/collector.py     主采集流程           │  │
│  │  app/data_collector/review_parser.py  LLM评测解析         │  │
│  │  app/data_collector/product_list.py   预定义产品清单       │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │                                       │
├─────────────────────────┼───────────────────────────────────────┤
│                    数据层                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  app/models/product.py   SQLAlchemy + Pydantic 模型       │  │
│  │  app/db/database.py      数据库操作 (CRUD)                │  │
│  │  data/cache.db           SQLite 数据库文件                 │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、详细模块说明

### 3.1 对话状态机 (`app/core/chat_manager.py`)

**ChatManager** 是整个系统的中枢协调器。

#### 状态流转

```
用户输入
  │
  ▼
[LLM 意图分析]
  ├─ 设备类型识别 (笔记本/台式机/都推荐)
  ├─ 约束提取 (预算/用途/品牌)
  └─ 是否需要追问?
       ├─ 是 → 返回追问，等待用户回答 → 回到分析
       └─ 否 → 进入下一步
  │
  ▼
[检查缺失信息]
  ├─ 没有指定用途? → 追问
  ├─ 没有预算? → 追问
  └─ 信息完整 → 进入下一步
  │
  ▼
[查询聚合评分数据库]
  ├─ 按设备类型 + 品牌过滤 SQL
  ├─ 价格 ±1000 严格过滤
  └─ 无结果则放松预算重新查
  │
  ▼
[多维度评分排序]
  ├─ 评测聚合分 (50%)
  ├─ 价格匹配度 (25%)
  ├─ 人群匹配度 (25%)
  └─ 评测数量加分 (封顶 0.5)
  │
  ▼
[组装推荐响应]
  ├─ 价格排序表格
  ├─ 雷达图数据
  ├─ 产品卡片 (含评分明细)
  └─ 追问引导按钮
```

#### 意图分析降级策略

```
LLM (MiniMax/DeepSeek/OpenAI)
  ├─ 优先使用 response_format JSON 模式
  ├─ 失败 → 降级为 prompt 要求 JSON 输出
  └─ 再失败 → 关键词匹配降级: _fallback_intent()
       ├─ 设备类型: 关键词匹配
       ├─ 预算: 正则提取 (5000元/5千/5000以内)
       ├─ 用途: 关键词映射 (游戏/编程/办公)
       └─ 品牌: 品牌名单匹配
```

---

### 3.2 聚合评分引擎 (`app/recommend/aggregator.py`)

这是替换电商评分的核心模块。

#### 数据来源权重

| 来源类型 | 权重 | 说明 |
|---------|------|------|
| 视频评测 (B站/YouTube) | 50% | 评测最真实，能看到实际表现 |
| 图文评测 (知乎/值得买) | 30% | 深度体验文，优缺点分析到位 |
| 论坛讨论 (贴吧/Chiphell) | 10% | 用户真实反馈 |
| 电商评价 (仅差评/追评) | 10% | 仅供参考 |

#### 评分维度

| 维度 | 说明 | 数据来源 |
|------|------|---------|
| 性能 | CPU/GPU 跑分和游戏表现 | 评测内容 LLM 提取 |
| 散热 | 满载温度、噪音、长期使用反馈 | 评测内容 LLM 提取 |
| 屏幕 | 分辨率、色域、亮度、刷新率 | 评测内容 LLM 提取 |
| 续航 | 实际使用续航测试 | 评测内容 LLM 提取 |
| 做工 | 机身质感、键盘、接口布局 | 评测内容 LLM 提取 |

#### 评分计算公式

```
综合评分 = 评测聚合分 × 0.5 + 价格匹配度 × 0.25 + 人群匹配度 × 0.25 + 评测数加分

各维度分 = 从评测原文中由 LLM 提取分析得出，非电商评分
```

#### 评分明细展示

每个产品卡片底部可展开"评分明细"，展示每条来源的评价和分数影响：

```
基础分 5.0
  📹 B站-笔吧评测室: 性能评分8.5  +1.4
  📝 知乎-硬件话题精选: 做工评分8.0  +0.6  
  💬 Chiphell-用户实测: 做工评分8.0  +0.3
  ─────────────────────────────
  基础分5.0 + 各源加权分 = 8.6
```

---

### 3.3 数据层 (`app/models/product.py`)

#### 数据模型关系

```
ProductModel (产品)
  ├── id (PK)
  ├── brand, series, model_name
  ├── device_type (笔记本/台式机)
  ├── price, original_price
  └── specs_json (配置信息)
       │
       ├── ReviewModel (评测来源)
       │     ├── product_id (FK)
       │     ├── source_type (video/article/ecommerce/forum)
       │     ├── source_name (B站/知乎/京东)
       │     ├── summary (LLM提取摘要)
       │     ├── pros_json, cons_json
       │     └── sentiment (positive/neutral/negative)
       │
       └── AggregatedScoreModel (聚合评分)
             ├── product_id (FK, unique)
             ├── overall_score (综合评分)
             ├── performance/thermal/display/battery/build_score
             ├── total_reviews, video_reviews, article_reviews
             ├── common_pros_json, common_cons_json
             └── suitable_for_json
```

---

### 3.4 前端交互 (`static/js/`)

#### WebSocket 消息协议

```
客户端 → 服务端:
  {"type":"message", "content":"5000元笔记本推荐", "session_id":"abc123"}

服务端 → 客户端:
  {"type":"connected", "session_id":"abc123"}
  {"type":"status", "content":"正在分析需求..."}
  {"type":"clarify", "content":"追问内容", "options":["选项A","选项B"]}
  {"type":"recommendation", "content":{summary, products, charts}}
  {"type":"error", "content":"错误信息"}
```

#### 等待体验优化

- 每次等待时显示随机电脑冷知识，每 5 秒轮换
- 共 28 条知识，覆盖硬件、游戏、保养、科技趋势
- 状态更新时保留当前冷知识，不影响阅读

---

### 3.5 数据采集 (`scripts/collect_reviews.py`)

可选的一键采集脚本，需要 Tavily API Key：

```
python scripts/collect_reviews.py
```

流程：
1. 从 `product_list.py` 读取 80 款笔记本 + 20 款台式机
2. 对每款产品搜索 "评测 优缺点"、"值得买吗"、"测评"
3. LLM 提取每篇评测的结构化数据
4. 聚合所有评测得到各维度评分
5. 存入 SQLite 数据库

---

## 四、文件结构

```
网络评测笔记本电脑/
├── app/                              # 后端 Python 包
│   ├── __init__.py
│   ├── main.py                       # FastAPI 入口 + 路由
│   ├── config.py                     # 配置管理 (pydantic-settings)
│   │
│   ├── api/                          # API 端点
│   │   ├── chat.py                   # WebSocket 聊天 (核心端点)
│   │   └── health.py                 # 健康检查
│   │
│   ├── core/                         # 对话核心
│   │   ├── chat_manager.py           # 对话状态机 (核心编排)
│   │   ├── conversation.py           # 会话状态定义
│   │   └── session_store.py          # 会话内存存储 (自动清理)
│   │
│   ├── llm/                          # LLM 交互
│   │   ├── client.py                 # OpenAI SDK 封装 (含降级)
│   │   ├── prompts.py                # 系统提示词模板
│   │   └── parsers.py                # 结果解析 (三重容错)
│   │
│   ├── search/                       # 搜索模块
│   │   ├── engine.py                 # 搜索抽象接口
│   │   ├── tavily_engine.py          # Tavily 实现
│   │   ├── query_builder.py          # 搜索查询生成
│   │   └── cache.py                  # LRU 缓存
│   │
│   ├── recommend/                    # 推荐引擎
│   │   └── aggregator.py            # 多源聚合评分 + 排序
│   │
│   ├── data_collector/               # 数据采集
│   │   ├── collector.py              # 主采集流程
│   │   ├── review_parser.py          # LLM 评测内容解析
│   │   └── product_list.py           # 80+20 产品口袋名单
│   │
│   ├── models/                       # 数据模型
│   │   ├── __init__.py               # 枚举 (DeviceType/UserGroup)
│   │   └── product.py                # SQLAlchemy + Pydantic 模型
│   │
│   └── db/                           # 数据库操作
│       └── database.py               # CRUD 操作
│
├── static/                           # 前端静态资源
│   ├── css/
│   │   ├── style.css                 # 全局样式
│   │   ├── chat.css                  # 聊天框样式
│   │   └── cards.css                 # 产品卡片样式
│   └── js/
│       ├── app.js                    # 应用入口 + WebSocket
│       ├── chat.js                   # 消息渲染 + 图表 + 评分明细
│       ├── charts.js                 # Chart.js (保留)
│       ├── cards.js                  # 卡片 (保留)
│       └── utils.js                  # 工具函数
│
├── templates/
│   └── index.html                    # SPA 主页面
│
├── scripts/
│   ├── seed_data.py                  # 种子数据导入 (20款产品)
│   └── collect_reviews.py            # 联网数据采集
│
├── data/                             # SQLite 数据库目录
├── requirements.txt                  # 依赖清单
├── .env                              # 密钥配置
├── run.py                            # 启动脚本
└── README.md                         # 使用文档
```

---

## 五、技术栈

| 层 | 选型 | 版本 | 说明 |
|---|------|------|------|
| Web 框架 | FastAPI | ≥0.137 | 原生 async，WebSocket 内置 |
| 运行时 | uvicorn | ≥0.49 | ASGI 服务器 |
| 数据库 | SQLite + SQLAlchemy | ≥2.0 | 零配置单文件 |
| LLM SDK | OpenAI SDK | ≥2.43 | 兼容 DeepSeek/Qwen 等 |
| 联网搜索 | Tavily | ≥0.5 | 专为 AI Agent 设计的搜索 API |
| 前端图表 | Chart.js | 4.4.1 | CDN 引入 |
| 前端交互 | 原生 WebSocket | - | 无框架依赖 |
| 数据校验 | Pydantic | ≥2.13 | 请求/响应校验 |
| 配置管理 | pydantic-settings | ≥2.14 | 环境变量配置 |

---

## 六、关键设计决策

### 6.1 为什么不用电商评分

电商平台评分注水严重（刷单、默认好评），因此本系统采用：
- 优先采集**视频评测**内容（B站/YouTube），权重 50%
- 其次**图文深度评测**（知乎/值得买），权重 30%
- 论坛讨论和电商差评仅作为辅助参考

### 6.2 为什么不用实时爬虫

反爬机制复杂，维护成本高，因此采用：
- **种子数据**：内置 20 款热门产品的预聚合评分，开箱即用
- **Tavily API**：按需搜索，结构化返回结果
- **LLM 解析**：搜索结果由 LLM 提取结构化评价

### 6.3 为什么选用 WebSocket

- 实时双向通信，服务器可推送状态更新和冷知识
- 相比 SSE，WebSocket 支持客户端到服务端的流式交互
- 无轮询开销，适合持续对话场景

### 6.4 多轮对话的品牌保持

用户追问 "联想呢" 时：
1. 保留上一轮的预算/用途约束
2. 只替换品牌过滤条件
3. 空品牌列表不覆盖已有品牌

---

## 七、部署方案

### 本地运行

```bash
python run.py
# 浏览器打开 http://localhost:3001
```

### 局域网访问

`.env` 中设置 `APP_HOST=0.0.0.0`，同一网络下其他设备通过 `http://<本机IP>:3001` 访问。

### 云部署

本应用是纯 Python Web 应用，可部署到：
- **Railway**：连接 GitHub 仓库，设置环境变量
- **Render**：Web Service 类型
- **Docker**：自行打包容器

---

## 八、风险与优化方向

### 已知风险

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| 数据覆盖不足 | 种子数据仅 20 款产品 | 可运行采集脚本扩充 |
| LLM Hallucination | LLM 可能编造评测内容 | 三重解析容错 + 来源标注 |
| 搜索依赖 | Tavily 搜索依赖外部 API | 无 API 时使用种子数据 |
| 评分偏差 | 少量评测可能不具代表性 | 视频评测权重最高 |

### 后续优化

- [ ] 增加更多种子产品数据（50+ 款）
- [ ] 支持从京东/B站直接抓取价格
- [ ] 产品价格可定期自动更新
- [ ] 用户反馈机制：用户可对推荐结果评分
- [ ] 多轮对话追问历史支持回退
- [ ] 产品对比功能：用户选择多款进行详细对比


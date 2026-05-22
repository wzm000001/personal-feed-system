---
purpose: 用户档案 · 每次 daily-digest 必读 · AI 导师的"记忆基础"
last_updated: 2026-05-22
update_frequency: 用户对话有新信息时立即更新
---

# 用户档案 · <User Name>

> **AI 导师 own 这个文件**。每次定时推送前必读，确保对用户的理解持续 fresh。

---

## 基础信息

| 字段 | 值 |
|---|---|
| 姓名 | <User Name> (用户名 <github-username>) |
| 邮箱 | <email> |
| 工作 | **大数据开发工程师** |
| 当前项目 | `<your-current-project>`（业务数据 + AI 知识库设计） |
| 设备 | macOS ARM64 (M 系列芯片) |
| 时区 | Asia/Shanghai (UTC+8) |

---

## AI 兴趣与目标

### 总体定位
- **AI 全方面感兴趣** —— 不要 filter 任何 AI 主题
- 关心 AI 怎么在**日常生活**中提效
- 想成为**最懂 AI 的前 10%**（有 AI 焦虑驱动）
- 关心 AI 落地应用（不只理论）

### 关注的具体方向（优先级排）

1. **AI 工程实战**：怎么用 AI 干活、Claude Code / Cursor 玩法、Prompt engineering
2. **Agent 系统**：Agent 工程化、brain/hands 解耦、harness 设计、MCP 协议
3. **AI 副业方向**（重点）：
   - AI 技术分享博主（X / 公众号 / 视频）
   - AI 应用开发（skill、插件、Web、小程序、APP）
   - 个人用 + 商业卖（B2B / B2C）
4. **大牛工作流**：Karpathy 怎么用 LLM、Anthropic 怎么设计 Claude Code、其他顶级 builder 的 AI 用法
5. **前沿理念**：AI 大项目设计思路、AI 应用落地的反直觉判断

### 跳过的内容
- 无 substantive 的 engagement bait（如 Sam Altman "你最希望 AI 解决什么"）
- 非 AI 主题（FFmpeg 视频技术、政治、慰问等）
- 纯营销推广（自家 tutorial 推广无 insight 类）
- 行业八卦（VC 融资金额无技术含量）

---

## 当前真问题（动态，每周可能变化）

### 🔥 #1 [高] AI 维护的结构化知识页 / 业务知识库设计
- 项目 `<your-current-project>` 的核心
- 5/19 连续追问"中间这一层 AI 维护的结构化知识页是怎么设计出来的"
- 涉及业务指标 + RAG 架构

### 🧠 #2 [中] Agent harness / brain-hands 解耦
- vault `agentic-systems-theory` 标 low coverage
- 5/17 fork llm-wiki-compiler 修 3 个 bug（做 long-running agent app）

### 💰 #3 [中] AI 副业方向探索
- 已 follow 黄赟、Indie Fox、yihui_indie、烟花老师
- 想找具体可执行的副业入口

### 📚 #4 [中] AI 系统知识深化（前 10% 目标）
- Karpathy / Anthropic / Lilian Weng 的一手思想
- vault concept `tool-stack-layering` 已写但需 evergreen 补充

### 🧘 #5 [低] 财富思维 / 心学
- weread 5/18-19 读《纳瓦尔宝典》《富爸爸穷爸爸》《王阳明心学》
- **focus AI 后此项弱化**（仅 PROFILE 信号，不进推送）

---

## 内容偏好

| 维度 | 偏好 |
|---|---|
| 语言 | 中文为主，关键术语保留英文（agent、harness、context、RAG、MCP、LLM、prompt、token、fine-tune、transformer、embedding、inference、sandbox、RLHF、multimodal 等） |
| 双语 | 不要 EN 段 + ZH 段对照，**只要中文版**（必要术语穿插英文） |
| 篇幅 | 不限推送量，但要有价值（无价值的不推也不存） |
| 时效 | 硬限制 < 30 天 + Evergreen 白名单例外（必须明确标注"X 个月前"或"X 年前"） |
| 媒介 | 全部 — 文字 / 视频 / 播客 / GitHub / 中文圈都要 |
| 深度 | Tier 1 深度（讲什么 + 价值点 + 启发 + 思考点）；Tier 2 中度（总结 + 启发）；Tier 3 简短（标题 + 总结 + 价值点） |

### HTML 输出要求
- 不是纯文字
- 借鉴 [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) 设计：
  - 滚动模块化（4-6 个 module）
  - 可视化（图表、数据流动画、对比图）
  - Code ↔ 中文左右对照
  - Quiz / 思考测试（每条推荐 1 个）
  - 术语 tooltip（hover 看解释）
  - Group Chat Animation（人物对话风格展示对比观点）
- 单页 HTML 文件，inline CSS/JS，可离线打开

---

## 技术栈

### 已用工具
- Claude Code（VSCode 扩展 v2.1.145 + 桌面 app v2.1.138）
- OpenClaw（已装但 channel 未配）
- Obsidian + llm-wiki-compiler（已 fork + 修 3 bug）
- Field Theory CLI（已收 72+ X bookmarks）
- Claude in Chrome MCP（已配对）
- Playwright MCP
- 各种 skill：weread / redbook / follow-builders / 多个 lark-* / codebase-to-course / frontend-slides / beautiful-html-templates

### 技能栈（推测）
- 大数据：Spark / Flink / Python / Scala / SQL
- 已用 AI 工具：Claude Code、Cursor、Codex
- Vault PKM：高级用户（17 topic / 73 source / 3 concept）

---

## Vault 状态摘要（5/22）

| Topic | Coverage | 备注 |
|---|---|---|
| claude-code | 🟢 high (10 src) | 持续主战场 |
| browser-automation | 🟢 high (8 src) | — |
| ai-side-business | 🟢 high (7 src) | 副业 |
| ai-industry-watch | 🟡 medium (23 src) | 多数 tweet 正文未抓 |
| viral-templates | 🟡 medium (2 src) | — |
| obsidian-pkm | 🟡 medium (4 src) | vault 自身 |
| skills-ecosystem | 🟡 medium (11 src) | 增长中 |
| ai-coding-agents | 🟡 medium (5 src) | — |
| **agentic-systems-theory** | 🔴 **low** (2 src) | **核心 gap，需补** |
| content-workflow | 🔴 low (3 src) | — |
| xiaohongshu-ops | 🔴 low (3 src) | — |
| prompt-engineering | 🔴 low (2 src) | — |
| ai-learning-path | 🔴 low (1 src) | — |
| product-ideas | 🔴 low (1 src) | — |
| workflow-tools | 🔴 low (1 src) | — |
| web-scraping | 🔴 low (2 src) | — |
| mcp-protocol | 🌱 seeded | 0 src |

**Concepts**：tool-stack-layering / mcp-vs-cli / info-arbitrage

**LOG 最新**：2026-05-17（**5/18-5/22 未沉淀进 vault** ⚠️）

---

## AI 导师每次推送前必做的事

1. **Read 此文件**（当前真问题 / 兴趣方向 / vault 状态）
2. **扫描 Claude Code 最近 7 天 session**（`~/.claude/projects/*/`）—— 新增主题 → 更新本文件 #当前真问题
3. **扫描 vault 最近 mtime 文件**（`$VAULT/01-Sources/` + `00-Wiki/LOG.md`）—— 新沉淀 → 更新本文件 #vault 状态
4. **基于上面 3 步**，每条推荐的"引发的思考"必须**点名连接到本档案的具体字段**（如"data-bp 项目"、"agentic-systems-theory low coverage"、"想做 AI 副业"等）

---

## 持续学习闭环

```
推送 (Discord + HTML)
    ↓
用户读完
    ↓
回答 Tier 1 quiz / 思考题（写到 vault 对应 topic）
    ↓
vault topic coverage 升级（如 agentic-systems-theory low → medium）
    ↓
下次推送时 PROFILE 反映新状态（不重复推已答的方向）
    ↓
推荐质量持续 calibrate
```

---

## 用户给我的明确指令（历史决策）

- 2026-05-17：不要让我贴 webhook URL 到对话（已部分泄露过，要轮换）
- 2026-05-22 早：focus AI，删 weread 信号
- 2026-05-22 中：AI 导师 own 价值判断，不让我做判断
- 2026-05-22 晚：只中文版（删 EN 双语段）；时效必须明确标注；Tier 3 也要有价值；HTML 要可视化（参考 codebase-to-course）

---

## 更新机制

- AI 导师在每次 daily-digest 时**主动更新**本文件
- 用户对话有新角色信息时立即更新
- 用户也可以手动改这个文件（你 own，但用户 review）

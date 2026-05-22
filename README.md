# personal-feed-system

> 个性化 AI 阅读流：8 信号源理解你的真问题，多媒介推荐 5 分钟阅读块，自动推送飞书。

## 这是什么

一套**本地运行**的 AI 阅读助手，每天早 8 点：

1. **Observe**：扫你的本机 8 个信号源（git/Claude session/zsh history/Obsidian vault/微信读书/X bookmarks/VSCode/Chrome）→ 提炼你"当下真问题"
2. **Route**：按问题主题路由信源池（80+ 源，按优先级权重排序）
3. **Fetch**：从 RSS / GitHub Atom / YouTube / 播客 / 中文圈 / SPA 站点并发抓取
4. **Match**：选 1 主推 + 2 备选，强制至少 3 种媒介
5. **Digest**：双语输出（关键术语保留英文）+ 三个读后反问 + 落点建议
6. **Push**：推送到飞书"文件传输助手"

灵感来自 [Zara Zhang 的 follow-builders](https://github.com/zarazhangrui/follow-builders)（追踪 AI Builder 不追网红），但把"中心化推送"升级为"个性化+本地+多源融合"。

## 设计哲学

| 维度 | 这个项目 |
|---|---|
| 信源治理权 | 用户（不是平台算法） |
| 信源池 | 80+ 源混合，Zara 名单 ⭐⭐⭐ 优先 |
| 匹配机制 | 真问题驱动（不是"今日新内容"） |
| 输出 | 中英双语，关键术语保留英文 |
| 隐私 | 全本地，0 个 API key 需要（除非用飞书推送） |
| 可审计 | 每篇推荐附"为什么这一篇"的证据链 |
| 闭环 | 三个反问 → 用户写答案到 vault → 形成正反馈 |

## 文件结构

```
personal-feed-system/
├── reading-feeds.md            # 信源池配置（你自己增删）
├── commands/
│   └── feed.md                 # Claude Code slash command
├── feed-prompts/               # 模块化摘要 prompt
│   ├── digest-intro.md
│   ├── summarize-blogs.md
│   ├── summarize-podcast.md
│   ├── summarize-tweets.md
│   └── translate.md
├── scripts/
│   └── feed-daily.sh           # 每日定时推送脚本
├── LaunchAgents/
│   └── com.example.feed-daily.plist  # launchd 定时任务
├── INSTALL.md                  # 安装指南
└── README.md
```

## 8 信号源融合

每次 `/feed` 触发时融合以下 8 个本机信号：

| # | 信号源 | 反映什么 |
|---|---|---|
| 1 | Git 最近 7 天 commits | 真做了什么 |
| 2 | Claude Code session 最近 14 天 | 卡在什么、问了什么 |
| 3 | Zsh history 最近 500 条 | 实际敲了什么命令 |
| 4 | VSCode 最近打开文件 | 在编辑什么 |
| 5 | Obsidian vault（LOG/INDEX/topics/concepts） | 在沉淀什么 |
| 6 | 微信读书 API（书架 + 划线） | 主动学习什么 |
| 7 | X bookmarks（如你用 Field Theory CLI） | 主动收藏什么 |
| 8 | Chrome 浏览历史（通过 Claude in Chrome MCP） | 主动浏览什么 |

## 信源池（80+ 源）

按优先级分 7 档：

1. **⭐⭐⭐ Zara 中心化 feed** — 25 个 AI Builder + 6 顶级播客 + 2 官方 blog（来自 [follow-builders skill](https://github.com/zarazhangrui/follow-builders)）
2. **⭐⭐ AI 工程评论博客** — Simon Willison / Lilian Weng / Eugene Yan / Hamel Husain / Chip Huyen
3. **⭐⭐ AI Newsletter** — Import AI / Interconnects / One Useful Thing / Last Week in AI
4. **⭐⭐ Agent/Skill 专题** — Anthropic Engineering / Building Effective Agents / MCP Spec
5. **⭐ YouTube 频道** — 3Blue1Brown / Karpathy / Yannic / Lex Fridman / Dwarkesh
6. **⭐ GitHub Release** — claude-code / anthropic-cookbook / mcp-servers / vllm
7. **⭐ 中文 AI 圈** — 向阳乔木 / 宝玉 / 量子位 / 机器之心 / B 站 UP 主 / 小红书

完整列表见 [reading-feeds.md](./reading-feeds.md)。

## 输出示例

```markdown
## 主推 🥇  📄 文字

### How to Work and Compound with AI
### 如何与 AI 协作并复利成长
- 来源：Eugene Yan · 文字 · 半衰期 1-2 年
- 发布：5 天前
- 估读：5 分钟
- 核心：`context as infra, taste as config` — 上下文是基础设施，品味是配置

#### 为什么这一篇（证据链）
1. 直接命中你真问题 #2：你昨天追问的 "AI 维护的结构化知识页"
2. 匹配你 vault concept `tool-stack-layering`
3. 时效完美 + 作者权威（Amazon staff applied scientist）

#### 读后三问
1. Eugene 的 `context/taste` 二分如何对应你 data-bp 项目里的"AI 知识页"？
2. 你最薄弱是 infra 层还是 config 层？
3. 明天再让 Claude 读项目时改一个什么提问角度？

#### 落点
读完写到 `$VAULT/00-Wiki/concepts/tool-stack-layering.md`
```

## 依赖

- **必需**：Claude Code (CLI)、Obsidian vault、`curl`/`python3`/`gh`
- **可选**：
  - [follow-builders skill](https://github.com/zarazhangrui/follow-builders) — Zara 中心化 feed（强烈推荐）
  - `yt-dlp` — YouTube 字幕（仅在你想看视频精华时用）
  - `lark-cli` + `lark-im` skill — 飞书推送
  - Claude in Chrome MCP — B 站等 SPA 站点抓取
  - `redbook` skill — 小红书抓取

## 安装

见 [INSTALL.md](./INSTALL.md)。

## 与 Zara follow-builders 的差异

| 维度 | Zara follow-builders | personal-feed-system |
|---|---|---|
| 理念 | 追建造者，不追网红 | 8 信号源融合理解你 |
| 信源数 | 33（25 X + 6 播客 + 2 blog） | 80+ |
| 信源类型 | X / 播客 / 官方 blog | + YouTube / GitHub / 中文 / 小红书 / B 站 |
| 匹配机制 | 全推送 | 真问题驱动 |
| 个性化 | 摘要风格可调 | 信源 + 匹配 + 摘要全可调 |
| 抓取 | 中心化（她团队抓） | 本地为主 + 消费 Zara feed |
| 推送 | Telegram / 邮件 | 飞书 / 邮件 |
| 翻译 | 英→中 | 中英双语 |
| 适合 | 想看 AI 圈共识 | 想看"对我而言"的内容 |

**两个项目可以同时用**：装 Zara skill 拿她的 feed，本系统消费它当 ⭐⭐⭐ 优先源。

## License

MIT — 自由复制 / 修改 / 商用 / 分发。

## 致谢

- [@zarazhangrui](https://x.com/zarazhangrui) 的 follow-builders 提供了核心信源 + 摘要 prompt 模板
- [@karpathy](https://x.com/karpathy) 的 LLM 工作流方法论
- Anthropic 的 Claude Code + Skills 生态

# personal-feed-system v6

> 个性化 AI 阅读流 · **AI 导师驱动** · 多媒介推荐 · 可视化 HTML 杂志 · 自动推送 Discord

## 核心理念

**AI 导师 own 价值判断**，用户消费 + 反馈。反对信息茧房——AI 不基于用户偏好递归强化推荐，而是基于行业客观价值 + 用户认知盲区主动推送。

## 工作流

```
launchd (每天 8 AM)
    ↓
daily-digest.sh → claude -p
    ↓
Stage 0: 读 user-profile.md ⭐（持续了解用户）
Stage 1: 抓 92 信源（Zara 33 + 中文 28 + 英文博客 + Newsletter + GitHub + YouTube + 播客）
Stage 2: 3 维 Value 打分（Primary × 0.3 + Influence × 0.4 + Recency × 0.3）
Stage 3: 时效硬限制 < 30 天 + Evergreen 白名单（12 篇 weekly rotate）
Stage 4: 3-tier 分级（都有价值，区别在投入时间）
Stage 5: 总结写法（Tier 1 含 Quiz · Tier 2 含启发 · Tier 3 含价值点）
Stage 6: 中文为主 + 关键术语英文
Stage 7: HTML 杂志生成（codebase-to-course 风格：滚动导航 + Group Chat + SVG + Tooltip + Quiz 折叠）
Stage 8: Discord 推送（webhook ?wait=true 顺序保证）
Stage 9: vault 存档 reading-log/{date}.md + .html
Stage 10: 主动更新 user-profile.md
```

## 文件结构

```
personal-feed-system/
├── README.md                       # 你在看
├── INSTALL.md                      # 安装指南
├── user-profile.md                 # 用户档案模板（v6 新增）
├── reading-feeds.md                # 92 信源全集
├── daily-digest-prompt.md          # 每天 8 AM 执行的完整指令（v6）
├── feed-prompts/                   # 5 个模块化 prompt（Zara 借鉴）
│   ├── digest-intro.md
│   ├── summarize-blogs.md
│   ├── summarize-podcast.md
│   ├── summarize-tweets.md
│   └── translate.md
├── scripts/
│   └── daily-digest.sh             # macOS launchd 触发脚本
├── LaunchAgents/
│   └── com.example.daily-digest.plist
├── examples/
│   └── sample-digest.html          # v6 HTML 杂志样例（codebase-to-course 风格）
└── LICENSE                         # MIT
```

## v6 新增

| 改进 | 描述 |
|---|---|
| 👤 **用户档案** | `user-profile.md` 持久化用户角色 / 兴趣 / vault 状态。每次推送前必读 |
| ⏳ **时效精准** | 必须标"X 个月前/X 年前"，杜绝 1 年前内容标"3 月前" |
| 🟢 **Tier 3 都有价值** | 删除"被过滤"项，Tier 区别 = 投入时间，不是有没有价值 |
| 🎨 **可视化 HTML** | 借鉴 [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course)：滚动导航 + Group Chat + SVG + Tooltip + Quiz |
| 🎯 **Quiz 测试理解** | 每条 Tier 1 含 quiz（不是问"它讲什么"，是问"应用到你场景"） |
| 🧠 **深度总结** | 讲什么 / 价值点 / 引发思考 / 带着思考去读（cite 用户档案具体字段） |

## 与 Zara follow-builders 关系

```
Zara follow-builders                  personal-feed-system
─────────────────────                 ──────────────────────
中心化抓 25 builder + 6 播客 + 2 blog  → 消费她的 feed-x.json
全推送，不个性化                       + 80+ 个补充信源
                                      + 用户档案驱动的深度总结
                                      + 可视化 HTML 杂志
                                      + 多 Tier 分级
                                      + 主动更新档案
```

**Zara 给"原料"，本系统给"按你口味的厨子"**。

## 关键设计：反信息茧房

普通推荐算法 = 强化用户偏好 = 视野收窄
AI 导师模式 = 基于客观价值 + 用户认知盲区主动推送 = 视野扩张

每条推荐附"为什么推这条"的证据链（cite 用户档案具体字段），用户能审计 AI 的判断，calibrate AI 的偏好。

## 安装

见 [INSTALL.md](./INSTALL.md)。

## License

MIT

---
purpose: v4 信源全集（AI 导师持有，用户不改）
last_updated: 2026-05-22
status: AI 导师 own，用户只看不改
focus: AI · 英文为主 · 中文 28 个 KOL 补充
total_sources: 92
delivery: Discord webhook（每天 8 AM）+ vault 存档
---

# Reading Feeds · v4 信源全集

**给 daily-digest 命令读的信源池。** 92 个源分 5 个 Tier，价值打分 3 维后输出 Tier 1/2/3。

**用户不需要改这个文件** —— AI 导师 own 它。用户的工作是消费 + 反馈"今天推得好不好"，AI 导师据此迭代。

---

## ⭐⭐⭐ Tier S: Zara 超核心（33 源 · 不动）

直接消费 `~/.claude/skills/follow-builders/feed-x.json` 等本地缓存。

### 25 个 AI Builders（X / Twitter）
Karpathy / Swyx / Josh Woodward / Kevin Weil / Peter Yang / Nan Yu / Madhu Guru / Amanda Askell / Cat Wu / Thariq / Google Labs / Amjad Masad / Guillermo Rauch / Alex Albert / Aaron Levie / Ryo Lu / Garry Tan / Matt Turck / Zara Zhang / Nikunj Kothari / Peter Steinberger / Dan Shipper / Aditya Agarwal / Sam Altman / Claude

### 6 顶级播客（YouTube channel）
- Latent Space `UCxBcwypKK-W3GHd_RZ9FZrQ`
- Training Data (Sequoia) `playlist=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8`
- No Priors `UCSI7h9hydQ40K5MJHnCrQvw`
- Unsupervised Learning `UCUl-s_Vp-Kkk_XVyDylNwLA`
- MAD Podcast `UCQID78IY6EOojr5RUdD47MQ`
- AI & I `UC5AxZxJNdRleW0gl2S9yKwQ`

### 2 官方 Blog
- Anthropic Engineering
- Claude Blog

---

## ⭐⭐ Tier A: 英文个人博客 + Newsletter（17 源）

### 9 个人博客（侧重英文，AI 工程顶流）
| 博客 | RSS | 备注 |
|---|---|---|
| Simon Willison | `https://simonwillison.net/atom/everything/` | 每日更新 #must-read |
| Lilian Weng | `https://lilianweng.github.io/index.xml` | 深度 evergreen 一手 #must-read |
| Eugene Yan | `https://eugeneyan.com/rss/` | Amazon staff, applied ML/evals |
| Hamel Husain | `https://hamel.dev/index.xml` | applied ML, evals 顶级 |
| Chip Huyen | (无 RSS，WebFetch) | ML systems 架构 |
| Sebastian Raschka | `https://magazine.sebastianraschka.com/feed` | LLM internals 教学 |
| Jay Alammar | `https://jalammar.github.io/feed.xml` | LLM visualization 一手 |
| Karpathy GitHub gist | `https://gist.github.com/karpathy.atom` | 个人代码 + 思考 |
| Andrew Ng (deeplearning.ai) | `https://www.deeplearning.ai/the-batch/feed/` | The Batch newsletter |

### 8 Newsletter (Substack 等)
| Newsletter | RSS | 备注 |
|---|---|---|
| Import AI | `https://importai.substack.com/feed` | Jack Clark **Anthropic 联创** #must-read |
| Interconnects | `https://www.interconnects.ai/feed` | Nathan Lambert · RLHF 顶尖 |
| One Useful Thing | `https://www.oneusefulthing.org/feed` | Ethan Mollick · applied AI |
| Stratechery | `https://stratechery.passport.online/feed/rss/Z3DG7Yx2crBcKKv2GpAVoH` | Ben Thompson · 战略层 |
| Last Week in AI | `https://lastweekin.ai/feed` | 周度综合 |
| The AI Daily Brief | `https://rss.beehiiv.com/feeds/zHQNXhJBOG.xml` | 日度新闻 |
| Latent Space (newsletter) | `https://www.latent.space/feed` | swyx 写的版 |
| Lenny's Newsletter | `https://www.lennysnewsletter.com/feed` | 产品 |

---

## ⭐⭐ Tier B: 中文 KOL（28 人）

### B1. 工程实战派（7）
| KOL | 平台 | 标识 |
|---|---|---|
| 宝玉 @dotey | X / 微博 | Prompt engineering 顶尖 |
| 向阳乔木 @vista8 | X / 公众号 | AI 工具实操 |
| 黄赟 @huangyun_122 | X / 小红书 | AI 小生意系列 |
| 烟花老师 @teach_fireworks | X | AI 工作流 |
| op7418 | X / 小红书 | AI 工具评测 |
| yidabuilds | X | AI 独立开发实战 |
| AI 进化论-花生 | 公众号 | 工程实战 |

### B2. 产品创业派（5）
| KOL | 平台 | 标识 |
|---|---|---|
| yihui_indie | X | AI 独立开发 + 创作者经济 |
| Indie Fox | X | 出海 SaaS，年入 $100K |
| 哥飞 (gefei55) | X | 独立开发 + 网站矩阵 |
| 海拉鲁编程客 | X | AI 编程 + 独立开发 |
| nopinduoduo | X | 推文→公众号 3 分钟工作流 |

### B3. 资讯媒体派（6）
| KOL | 平台 | 标识 |
|---|---|---|
| 量子位 | 公众号 / 网站 | AI 综合 |
| 机器之心 | 公众号 / 网站 | AI 学术 + 产品 |
| 极客公园 | 公众号 / 网站 | 科技 + AI |
| 新智元 | 公众号 | AI 最新动态 |
| 知危 Deep | 公众号 | AI 深度访谈 |
| AI 寒武纪 | 公众号 | 最新动态 |

### B4. 思想评论派（5）
| KOL | 平台 | 标识 |
|---|---|---|
| orange.ai | X | AI 思想 + 产品判断 |
| 卡兹克 | X / 公众号 | AI 评论 + 产品测评 |
| 段小草 | X | AI 思想 |
| 阿稳 | X | AI 创业洞察 |
| Hito | X | AI 应用方向 |

### B5. 大牛一线（5）
| KOL | 平台 | 标识 |
|---|---|---|
| 李沐 (Mu Li) | B 站 / X | paper reading 中文最佳 |
| 翁荔 Lilian Weng | X / 个人博客 | 前 OpenAI（也在英文博客 Tier A） |
| 沈向洋 | X | 微软前 / AI 思想 + 战略 |
| 谢赛宁 | X | NYU · 计算机视觉 + multimodal |
| 吴恩达 Andrew Ng | X | deeplearning.ai · 应用 AI |

---

## ⭐ Tier C: 官方 Changelog + GitHub Release（19 源）

### 11 官方页（侧重一手 changelog）
| 源 | URL / 抓取方式 |
|---|---|
| Anthropic Engineering | https://www.anthropic.com/engineering (WebFetch) |
| Anthropic Research | https://www.anthropic.com/research |
| Anthropic News | https://www.anthropic.com/news |
| Claude Blog | https://claude.com/blog |
| Claude Code release notes | https://docs.claude.com/en/release-notes/claude-code |
| Anthropic API changelog | https://docs.claude.com/en/api/changelog |
| OpenAI Research | https://openai.com/research |
| OpenAI Cookbook recent | https://github.com/openai/openai-cookbook/commits.atom |
| DeepMind Blog | https://deepmind.google/discover/blog/ |
| Hugging Face Daily Papers | https://huggingface.co/papers |
| MCP Spec | https://modelcontextprotocol.io/ |

### 8 GitHub Release
| Repo | Atom URL |
|---|---|
| anthropics/claude-code | `https://github.com/anthropics/claude-code/releases.atom` |
| anthropics/anthropic-cookbook | `https://github.com/anthropics/anthropic-cookbook/commits.atom` |
| modelcontextprotocol/servers | `https://github.com/modelcontextprotocol/servers/commits.atom` |
| modelcontextprotocol/python-sdk | `https://github.com/modelcontextprotocol/python-sdk/releases.atom` |
| pydantic/pydantic-ai | `https://github.com/pydantic/pydantic-ai/releases.atom` |
| vllm-project/vllm | `https://github.com/vllm-project/vllm/releases.atom` |
| continuedev/continue | `https://github.com/continuedev/continue/releases.atom` |
| microsoft/playwright-mcp | `https://github.com/microsoft/playwright-mcp/releases.atom` |

---

## ⭐ Tier D: 视频 + 实时社区信号（11 源）

### 8 个 YouTube 频道（Zara 6 播客之外）
| 频道 | channel_id |
|---|---|
| 3Blue1Brown | `UCYO_jab_esuFRV4b17AJtAw` |
| Andrej Karpathy | `UCXUPKJO5MZQN11PqgIvyuvQ` |
| Yannic Kilcher | `UCZHmQk67mSJgfCCTn7xBfew` |
| Lex Fridman | `UCSHZKyawb77ixDdsGog4iWA` |
| Dwarkesh Patel | `UCXl4i9dYBrFOabk0xGmbkRA` |
| Two Minute Papers | (查) |
| Fireship | `UCsBjURrPoezykLs9EqgamOA` |
| AI Engineer (会议) | (查) |

RSS 模板：`https://www.youtube.com/feeds/videos.xml?channel_id=UCxxx`

### 4 个 Bilibili UP（中文视频）
| UP | mid |
|---|---|
| 李沐 (Mu Li) | 1567748478 |
| 林亦LYi | 477689080 |
| 影视飓风 | 946974 |
| 何同学 | 163637592 |

抓取：Claude in Chrome → `space.bilibili.com/<mid>/upload`

### 3 个实时社区
| 源 | RSS |
|---|---|
| HackerNews AI top | `https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+Anthropic&points=50` |
| r/LocalLLaMA | `https://www.reddit.com/r/LocalLLaMA/.rss` |
| Show HN | `https://hnrss.org/show` |

---

## ⭐⭐⭐⭐ Evergreen 必读白名单（rotate 推送，每周 1 篇）

绕过时效硬限制。8 篇核心 + 4 篇补充，推完一轮（约 3 月）后回到推完即停。

### 核心 8 篇
1. Karpathy: [Software 3.0 talk](https://www.youtube.com/watch?v=LCEmiRjPEtQ)
2. Karpathy: [Intro to LLMs 1hr talk](https://www.youtube.com/watch?v=zjkBMFhNj_g)
3. Karpathy: [zero-to-hero series](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)
4. Anthropic: [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
5. Lilian Weng: [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
6. Anthropic: [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)
7. Eugene Yan: [How to Work and Compound with AI](https://eugeneyan.com/writing/working-with-ai/)
8. Karpathy gist: [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

### 补充 4 篇
9. Lilian Weng: [Why We Think](https://lilianweng.github.io/posts/2025-05-01-thinking/)
10. Anthropic: [Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
11. Karpathy: [How I use LLMs](https://www.youtube.com/watch?v=EWvNQjAaOHw)
12. Jay Alammar: [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

---

## 价值打分公式（AI 导师执行）

每条候选内容打分 0-10，三个维度加权：

```
Value = (Primary × 0.3) + (Influence × 0.4) + (Recency × 0.3)
```

| 维度 | 10 分 | 5 分 | 0 分 |
|---|---|---|---|
| **Primary** 一手性 | builder 本人发的 / 官方 blog | 媒体报道 | 评论员转述 |
| **Influence** 影响力 | Zara 25 + 中文 KOL 28 白名单 / Anthropic 官方 | 业内有声 | 无名营销号 |
| **Recency** 时效 | < 24h | < 7d | > 30d 几乎过滤；evergreen 例外 |

**Substantive 二次过滤**（LLM remix 时）：
- 跳过：mundane / 转推无评论 / 推广 / 应酬
- 保留：原创观点 / 技术洞察 / 产品发布 / 行业分析 / 教训

---

## 3-Tier 分级（输出层）

| Tier | Value 阈值 | 输出形式 | 推送渠道 |
|---|---|---|---|
| 🔴 Tier 1 | ≥ 7 | 完整摘要 + 双语 + 反问 | Discord 推送 |
| 🟡 Tier 2 | 4-7 | 标题 + 一句话 + 链接 | Discord 推送 |
| 🟢 Tier 3 | < 4 | 仅标题 + 链接（元数据） | 仅 vault 存档 |

每天推送量：
- Tier 1：当天有几条算几条（没有就 0 条）
- Tier 2：约 5-15 条
- Tier 3：约 10-30 条（不推送，只入档）

---

## 双语规则

- 英文原标题保留 + 中文翻译标题
- 关键术语保留英文：LLM / agent / context / harness / RAG / fine-tune / token / prompt / sandbox / MCP / RLHF / inference / embedding / transformer / multimodal 等
- 专有名词保留英文：人名、产品名、公司名、产品代号
- 摘要：中文为主，英文金句段段对照
- 翻译 prompt 复用 Zara 的 `feed-prompts/translate.md`

---

## 维护节奏（AI 导师自驱）

- **每周**：扫死链 / 关注新冒出的 builder（如某人最近爆红）
- **每月**：评估 reading-log 价值反馈，淘汰长期 0 命中信源
- **每季**：evergreen 列表更新（推完一轮后加新经典）
- **半年**：架构反思（信源池 vs 价值打分是否需要重构）

用户反馈渠道：在 Discord 里回 "👎" 表情或文字反馈，AI 导师下次 digest 调权。

---

## 工具依赖

- ✅ Zara skill（feed-x.json 每天 07:32 自动更新）
- ✅ feed-prompts/（5 个模块化 prompt：digest-intro / summarize-* / translate）
- ✅ Discord webhook（已配 `~/.follow-builders/.env`）
- ✅ Claude in Chrome MCP（SPA fallback for Bilibili 等）
- ✅ redbook skill（小红书）
- ✅ `gh` / `curl` / `python3` / `yt-dlp`
- ✅ Claude Code scheduled-tasks（每天 8 AM 触发）

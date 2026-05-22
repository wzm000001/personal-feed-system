---
purpose: /feed 命令的订阅清单（v3 · focus AI + Zara优先 + 双语）
last_updated: 2026-05-22
status: living document
focus: AI builders & engineering（非 AI 主题已删除）
---

# Reading Feeds · 信源池 v3

**给 `/feed` 命令读的订阅清单。** focus AI，Zara 名单 ⭐⭐⭐ 最高优先，本地为辅。

---

## ⭐⭐⭐ 优先 1：Zara 中心化 Feed（每天自动更新）

**消费路径**：直接读本地文件，不用抓
```
~/.claude/skills/follow-builders/feed-x.json          # 25 个 builder 最近 24h 推文
~/.claude/skills/follow-builders/feed-podcasts.json   # 6 个播客最新集
~/.claude/skills/follow-builders/feed-blogs.json      # 2 个 blog 最新文章
```

**为什么最高优**：
- Zara 团队精选 25 个 AI builder（不是网红是真造产品的人）
- 中心化抓取（你电脑不用做事，每天 07:32 自动更新）
- 一手信源（builder 自己发的推文 vs 媒体转述）

**25 个 AI Builders**（来自 Zara 名单）：

| 类别 | 人物 |
|---|---|
| 🧠 大研究员 | Karpathy / Amanda Askell（Anthropic）/ Sam Altman / Claude 官号 |
| ⚙️ AI 工程顶级 | Swyx / Cat Wu（Anthropic）/ Alex Albert（Anthropic）/ Thariq |
| 🏢 CEO/创始人 | Amjad Masad（Replit）/ Garry Tan（YC）/ Aaron Levie（Box）/ Dan Shipper（Every）/ Aditya Agarwal |
| 📦 产品 | Josh Woodward（Google）/ Kevin Weil（OpenAI）/ Peter Yang / Nan Yu / Madhu Guru / Ryo Lu（Cursor）/ Peter Steinberger |
| 💰 VC/战略 | Matt Turck / Zara Zhang / Nikunj Kothari / Guillermo Rauch（Vercel） |
| 🏛️ 机构 | Google Labs |

**6 个顶级播客**（用 YouTube channel_id 拉 RSS）：

| 播客 | 主持 | channel_id |
|---|---|---|
| [Latent Space](https://www.youtube.com/@LatentSpacePod) | Swyx | `UCxBcwypKK-W3GHd_RZ9FZrQ` |
| [Training Data](https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8) | Sequoia | playlist_id |
| [No Priors](https://www.youtube.com/@NoPriorsPodcast) | Sarah Guo + Elad Gil | `UCSI7h9hydQ40K5MJHnCrQvw` |
| [Unsupervised Learning](https://www.youtube.com/@RedpointAI) | Jacob Effron | `UCUl-s_Vp-Kkk_XVyDylNwLA` |
| [The MAD Podcast](https://www.youtube.com/@DataDrivenNYC) | Matt Turck | `UCQID78IY6EOojr5RUdD47MQ` |
| [AI & I](https://www.youtube.com/@AIandI) | Dan Shipper | `UC5AxZxJNdRleW0gl2S9yKwQ` |

**2 个官方 blog**：
- [Anthropic Engineering](https://www.anthropic.com/engineering) #must-read
- [Claude Blog](https://claude.com/blog) #release #product

---

## ⭐⭐ 优先 2：AI 工程评论博客（个人观点，Zara 未覆盖）

每个源带 RSS URL，**curl 直接拉**。

- [Simon Willison](https://simonwillison.net/) [rss](https://simonwillison.net/atom/everything/) #daily #must-read
- [Lilian Weng](https://lilianweng.github.io/) [rss](https://lilianweng.github.io/index.xml) #deep #must-read
- [Eugene Yan](https://eugeneyan.com/writing/) [rss](https://eugeneyan.com/rss/) #applied-ml #evals
- [Hamel Husain](https://hamel.dev/) [rss](https://hamel.dev/index.xml) #applied-ml #evals
- [Chip Huyen](https://huyenchip.com/blog/) #ml-systems
- [Sebastian Raschka](https://magazine.sebastianraschka.com/) [rss](https://magazine.sebastianraschka.com/feed) #llm-internals
- [Jay Alammar](https://jalammar.github.io/) #visualization

---

## ⭐⭐ 优先 3：AI Newsletter

- [Import AI](https://importai.substack.com/) [rss](https://importai.substack.com/feed) #anthropic #jack-clark #must-read
- [Interconnects](https://www.interconnects.ai/) [rss](https://www.interconnects.ai/feed) #rlhf #nathan-lambert
- [One Useful Thing](https://www.oneusefulthing.org/) [rss](https://www.oneusefulthing.org/feed) #applied #ethan-mollick
- [The AI Daily Brief](https://aidailybrief.beehiiv.com/) [rss](https://rss.beehiiv.com/feeds/zHQNXhJBOG.xml) #daily-news
- [Last Week in AI](https://lastweekin.ai/) [rss](https://lastweekin.ai/feed) #weekly-digest

---

## ⭐⭐ 优先 4：Agent / Skill / MCP 专题

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) #must-read #agent-patterns
- [Claude Code release notes](https://docs.claude.com/en/release-notes/claude-code) #fresh
- [MCP Spec](https://modelcontextprotocol.io/) #protocol
- [Anthropic Research](https://www.anthropic.com/research) #safety #alignment
- [Anthropic News](https://www.anthropic.com/news) #release #model

---

## ⭐ 优先 5：YouTube 频道（补充 Zara 6 播客之外）

| 频道 | channel_id | tag |
|---|---|---|
| [3Blue1Brown](https://www.youtube.com/@3blue1brown) | `UCYO_jab_esuFRV4b17AJtAw` | #math #visualization |
| [Andrej Karpathy](https://www.youtube.com/@AndrejKarpathy) | `UCXUPKJO5MZQN11PqgIvyuvQ` | #llm-internals #must-watch |
| [Yannic Kilcher](https://www.youtube.com/@YannicKilcher) | `UCZHmQk67mSJgfCCTn7xBfew` | #paper-reading |
| [Lex Fridman](https://www.youtube.com/@lexfridman) | `UCSHZKyawb77ixDdsGog4iWA` | #long-interview |
| [Dwarkesh Patel](https://www.youtube.com/@DwarkeshPatel) | `UCXl4i9dYBrFOabk0xGmbkRA` | #ai-research-interview |
| [Two Minute Papers](https://www.youtube.com/@TwoMinutePapers) | — | #paper-tldr |
| [AI Engineer](https://www.youtube.com/@aiDotEngineer) | — | #conference-talks |

RSS URL 模板：`https://www.youtube.com/feeds/videos.xml?channel_id=UCxxx`

---

## ⭐ 优先 6：GitHub Release / Changelog（工具栈感知）

- [anthropics/claude-code](https://github.com/anthropics/claude-code) [atom](https://github.com/anthropics/claude-code/releases.atom) #must-watch
- [anthropics/anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) [atom](https://github.com/anthropics/anthropic-cookbook/commits.atom)
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) [atom](https://github.com/modelcontextprotocol/servers/commits.atom) #mcp
- [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) [atom](https://github.com/modelcontextprotocol/python-sdk/releases.atom) #mcp
- [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) [atom](https://github.com/microsoft/playwright-mcp/releases.atom) #browser
- [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai) [atom](https://github.com/pydantic/pydantic-ai/releases.atom) #agent-framework
- [vllm-project/vllm](https://github.com/vllm-project/vllm) [atom](https://github.com/vllm-project/vllm/releases.atom) #inference

---

## ⭐ 优先 7：中文 AI 圈（用户偏好保留）

- [向阳乔木 @vista8](https://yangchaomu.com/) #zh-ai #prompt
- [宝玉 @dotey](https://baoyu.io/) [rss](https://baoyu.io/atom.xml) #zh-ai-prompt
- [orange.ai](https://orange.ai/) #zh-ai
- [量子位](https://www.qbitai.com/) #zh-news
- [机器之心](https://www.jiqizhixin.com/) #zh-research-digest
- 你 vault `topics/ai-industry-watch.md` 已跟踪的 30+ 中文 KOL → 自动 ingest

### 📺 中文 Bilibili UP

| UP 主 | mid | tag |
|---|---|---|
| [李沐](https://space.bilibili.com/1567748478) | 1567748478 | #paper-reading #zh #must-watch |
| [林亦LYi](https://space.bilibili.com/477689080) | 477689080 | #ai-application |
| [何同学](https://space.bilibili.com/163637592) | 163637592 | #tech-product |
| [影视飓风](https://space.bilibili.com/946974) | 946974 | #content-creation |

### 📕 小红书（通过 redbook skill）

- @黄赟 `huangyun_122` #zh-ai-side-business
- @op7418 #zh-ai-tools
- @向阳乔木 / @vista8 #zh-ai-prompt
- @teach_fireworks #zh-ai-workflow

---

## 📰 实时信号

- [HackerNews AI 主题](https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+Anthropic&points=30) [rss](https://hnrss.org/newest?q=AI+OR+LLM+OR+Claude+OR+Anthropic&points=30) #ai-only
- [Show HN](https://hnrss.org/show) [rss](https://hnrss.org/show) #side-project
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/.rss) [rss](https://www.reddit.com/r/LocalLLaMA/.rss) #oss-llm
- [Hugging Face Daily Papers](https://huggingface.co/papers) #daily-papers
- 你 vault `01-Sources/x-bookmarks/` 已收藏的 72+ 条 #curated

---

## 已删除（v2→v3）

为 focus AI，**这些非 AI 主题源已删除**：

- 系统底层：Julia Evans / Dan Luu / Brendan Gregg / LWN / ByteByteGo
- 商业/独立开发：Indie Hackers / Sahil / Naval / Paul Graham / Levels.fyi
- PKM/思维：Andy Matuschak / Maggie Appleton / Gwern / Ness Labs
- arXiv firehose（信息量太大）

> 如果未来想恢复，看 v2（git history）。

---

## 给 /feed 的提示

### 信源优先级 → 权重 boost
- 优先 1 (Zara) → 权重 +50%
- 优先 2-3 (个人博客 + Newsletter) → +30%
- 优先 4 (Agent 专题) → +30%
- 优先 5-7 → 基准
- `#must-read` / `#must-watch` 再 +20%
- `#fresh` (< 7 天发布) → +20%

### 多样性强制
- 主推 + 备选 3 篇，**至少 3 种媒介**（X 推文 / 文字博客 / 视频 / 播客 / GitHub / 中文）
- 每日至少 1 篇 Zara 优先源命中
- 每周至少 1 篇中文源 + 1 个 GitHub Release

### 双语输出
- 英文源：保留英文原标题 + 中文翻译标题
- 关键术语保留英文（LLM / RAG / agent / context / harness 等）
- 摘要中文，金句中英对照

### 维护节奏
- 每周扫一次：删死链 / 加新源
- 每月评估：根据 `reading-log/` 历史看哪些源真给价值
- Zara 名单和 prompts 通过 `git pull ~/.claude/skills/follow-builders` 自动同步

---

## 工具依赖

- ✅ Zara skill (`~/.claude/skills/follow-builders/`)
- ✅ feed-prompts/ 模块化摘要（`$VAULT/00-Wiki/feed-prompts/`）
- ✅ Claude in Chrome MCP（B 站 / SPA fallback）
- ✅ redbook skill（小红书）
- ✅ lark-im / lark-mail（飞书推送）
- ✅ `gh` / `curl` / `python3` / `yt-dlp`

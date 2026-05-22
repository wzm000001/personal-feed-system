---
description: focus AI · 8 信号源融合理解你的真问题 · Zara 信源 ⭐⭐⭐ 优先 · 双语输出 · 多媒介 · 落到 reading-log 并可推送飞书
---

# /feed v3 · 个性化 AI 阅读流（focus AI + Zara优先 + 双语）

每次调用按 7 阶段严格执行。**不要跳步**。

## Vault 解析

`$LLM_WIKI_GLOBAL_DIR` 定位 vault。未设则提示 export。

## Arguments

- `$ARGUMENTS`（可选）：
  - 空 → 默认追加模式
  - 主题词如 `agent` / `prompt` / `evals` → 跳过 PROFILE 重观察，直接按主题路由
  - `--reset` → 覆盖今日文件
  - `--new` → 新建带序号文件
  - `--push` → 推送到飞书（lark-im 文件传输助手）
  - `--lang=en` → 仅英文（默认中英双语）

---

## Stage 1 · Observe（8 信号源融合）

并发提取（同 v2）：

| # | 源 | 路径/命令 |
|---|---|---|
| 1 | Git | `find ~/Documents ~/Desktop ~/code ~ -maxdepth 4 -name .git`，每个 `git log --since=7d` |
| 2 | Claude session | `find ~/.claude/projects -name "*.jsonl" -mtime -14` |
| 3 | Zsh history | `tail -500 ~/.zsh_history` 处理 |
| 4 | VSCode 最近 | `~/Library/Application Support/Code/User/globalStorage/storage.json` |
| 5 | Vault 全局 | LOG / INDEX / topics(-7d) / concepts / 90-Inbox / 01-Sources(-14d, ≤20) |
| 6 | Weread | `/shelf/sync` + `/user/notebooks`（API key），不输出 weread:// 链接 |
| 7 | X bookmarks | `find -L $VAULT/01-Sources/x-bookmarks -name "*.md"` |
| 8 | Chrome | `mcp__Claude_in_Chrome__list_connected_browsers` 非空可用 |

---

## Stage 2 · Synthesize Real Questions

融合 8 源 → **3-5 条"当下真问题"**：
- 问题描述（1-2 句，具体不空泛）
- 紧迫性 / 复杂度
- 证据链（≥ 2 个不同信号源）
- 主题 tag（用于 Stage 3 匹配）

**focus AI 提醒**：v3 信源池已删除非 AI 主题源。真问题如果命中非 AI（哲学/系统底层），标 `🚫 信源池不覆盖`，建议用 vault `topics/` 内部检索或 `/distill`。

---

## Stage 3 · Route + Boost（信源优先级）

读 `$VAULT/00-Wiki/reading-feeds.md`。按以下权重 boost 候选源：

| 优先级 | 权重 |
|---|---|
| **优先 1: Zara feed**（feed-x.json / feed-podcasts.json / feed-blogs.json） | +50% |
| **优先 2: AI 工程评论博客**（Simon/Lilian/Eugene/Hamel/Chip/Raschka） | +30% |
| **优先 3: AI Newsletter**（Import AI/Interconnects/One Useful Thing） | +30% |
| **优先 4: Agent/Skill 专题** | +30% |
| 优先 5-7（YouTube / GitHub / 中文） | 基准 |
| `#must-read` / `#must-watch` | +20% |
| `#fresh` (发布 < 7 天) | +20% |

---

## Stage 4 · Fetch（按源类型分发，Zara 优先消费）

### 🌟 Stage 4.0 · Zara Feed（最优先，零网络）

读三个本地 JSON：

```bash
ZARA_DIR=~/.claude/skills/follow-builders
python3 -c "
import json
x = json.load(open('$ZARA_DIR/feed-x.json'))
print(f'X: {len(x[\"x\"])} builder, generated {x[\"generatedAt\"]}')
for b in x['x']:
    for t in b['tweets']:
        # 每条推文 → 候选 source
        pass

p = json.load(open('$ZARA_DIR/feed-podcasts.json'))
b = json.load(open('$ZARA_DIR/feed-blogs.json'))
"
```

如果 Zara feed 不存在或不够新（generatedAt > 24h），降级到 Stage 4.1。

### Stage 4.1 · 其他源（RSS/Atom/API/SPA）

| 源类型 | 路径 |
|---|---|
| RSS / Atom | `curl -sL "$RSS_URL"` |
| GitHub releases | `curl -sL "https://github.com/X/Y/releases.atom"` 或 `gh api 'repos/X/Y/releases?per_page=5'`（**注意 URL 用单引号包**） |
| 普通 HTML 文章 | `WebFetch` |
| YouTube 频道 | RSS: `https://www.youtube.com/feeds/videos.xml?channel_id=UCxxx` |
| YouTube playlist | RSS: `https://www.youtube.com/feeds/videos.xml?playlist_id=PLxxx` |
| Bilibili UP | Claude in Chrome → `space.bilibili.com/<mid>/upload` → `get_page_text` |
| 小红书 KOL | redbook skill |
| 播客（YouTube 上的） | 同 YouTube 频道（用 channel_id） |

### 并发原则
- ≤ 8 个并发 fetch
- 只拿元数据 + 描述 200 字
- Top 5 候选再"细 fetch"拿 200-500 字摘要

### 失败降级
- 任何源失败 → 跳过，不让整个命令崩
- Zara feed 失败 → 退回纯本地源
- WebFetch HTTP 4xx → 跳过该源

### 排序公式
```
score = (语义相关性 × 0.5) + (时效 × 0.3) + (优先级权重) + (must-read boost) - (已推过去重)
```

---

## Stage 5 · Digest（生成推荐 + 双语）

选 **1 主推 + 2 备选**，**至少 3 种媒介**。

### 调用 prompts 模板

引用 `$VAULT/00-Wiki/feed-prompts/`：

| 媒介 | 用 prompt |
|---|---|
| X 推文 | `summarize-tweets.md` |
| 博客文章 | `summarize-blogs.md` |
| 播客 | `summarize-podcast.md` |
| Digest 总体格式 | `digest-intro.md` |
| 英→中翻译 | `translate.md` |

### 双语规则（默认 `--lang=zh-en`）

- **英文标题**：保留 + 中文翻译标题
- **关键术语**：保留英文（LLM / RAG / agent / context / harness / MCP / Claude Code / RLHF / fine-tune 等）
- **专有名词**：保留英文（人名、产品名、公司名）
- **摘要 + 推荐理由**：中文为主
- **金句**：中英对照展示

### 每篇必备字段
- 标题（英文 + 中文翻译）+ URL
- 来源（域名 + 媒介 emoji + 半衰期）
- 发布日期
- 估读/估看时长
- **「为什么这一篇」**：3+ 条证据链链回 Stage 1 信号
- **读后三问**（中文）
- **落点**：明确写入 vault 哪个文件

---

## Stage 6 · Output（reading-log 文件）

写入 `$VAULT/01-Sources/reading-log/{YYYY-MM-DD}.md`。

### 一天多次：默认追加 + 智能去重 + 递减输出

- 首次：全量（1 主推 + 2 备选 + 完整 PROFILE + 双语）
- 第 2+ 次：增量（1 主推 + 1 备选 + PROFILE diff）
- 读已有 `## 已推 URL 列表` 节做去重
- 跨日重置（新文件，去重列表清空）

### 文件结构

```markdown
---
type: reading-log
date: YYYY-MM-DD
generated_by: /feed v3
runs: N
sources_used: [...]
media_mix: [X/blog/podcast/video/github/zh]
lang: zh-en
---

# Reading Log · YYYY-MM-DD

## 第 N 次 · HH:MM [全量/增量]

### 当下真问题
...

### 主推 🥇 [媒介 emoji]
**EN:** [English Title](url)
**ZH:** [中文翻译标题]
（来源 / 发布日期 / 估读时长 / 半衰期）

#### 为什么这一篇（证据链）
...

#### 摘要（中文 + 关键术语保留英文）
...

#### 金句
> **EN:** ...
> **ZH:** ...

#### 读后三问
1. ...
2. ...
3. ...

#### 落点
读完写到 `$VAULT/...`

### 备选 🥈 [媒介 emoji]
...

### 备选 🥉 [媒介 emoji]
...

### PROFILE 快照
...

## 已推 URL 列表
- url1
- url2
```

### 写完后
- chat 简短：✅ + 主推标题 + 一句为什么 + URL
- 如果带 `--push`，进 Stage 7

---

## Stage 7 · 推送（可选）

### `--push` 触发飞书推送

用 **lark-im skill** 推到飞书"文件传输助手"或指定群：

```
1. 读 reading-log/{YYYY-MM-DD}.md
2. 提取"今日 5 分钟阅读块"摘要（不含完整 PROFILE 审计部分）
3. 用 lark-im 推送（消息体支持 markdown）
4. 推送成功后在 reading-log 文件追加 `pushed_at: YYYY-MM-DD HH:MM`
```

### 每日 8 点定时推送

通过 `mcp__scheduled-tasks__create_scheduled_task` 配置：
- cron: `0 8 * * *` (每天早 8 点)
- task: `/feed --push`
- 输出端：lark-im → 文件传输助手

详见 `update-config` skill 配置文档。

---

## 重要约束

| 约束 | 说明 |
|---|---|
| **focus AI** | v3 信源池只覆盖 AI。非 AI 真问题标 🚫 跳过 |
| **永不硬编码源** | 从 `reading-feeds.md` 读 |
| **永不推 weread://** | weread 仅作 PROFILE 信号 |
| **永不重复** | 当日 `## 已推 URL 列表` 去重 |
| **永远证据链** | 3+ 条具体证据，回链 Stage 1 |
| **多媒介** | 至少 3 种媒介 |
| **双语默认** | 关键术语保留英文 |
| **审计** | PROFILE 快照透明展示输入 |
| **不污染主流程** | 任何源失败降级 |

## 已装工具

- ✅ `curl` / `gh` / `python3` / `yt-dlp` (v2026.03.17)
- ✅ Claude in Chrome MCP（B 站 SPA fallback）
- ✅ redbook skill / lark-im / lark-mail
- ✅ follow-builders skill（Zara 中心化 feed，每天 07:32 自动更新）
- ✅ feed-prompts/（5 个模块化 prompt：digest-intro / summarize-blogs / summarize-podcast / summarize-tweets / translate）

## 调试 / 健康检查

定期跑：
```bash
# Zara feed 健康
stat -f "%Sm" ~/.claude/skills/follow-builders/feed-x.json  # 应该是今天
# RSS 死链
for url in $(grep -oE 'https?://[^ ]+/feed' $VAULT/00-Wiki/reading-feeds.md); do
  curl -sI "$url" | head -1
done
# vault PROFILE 完整性
ls $VAULT/00-Wiki/ $VAULT/01-Sources/reading-log/ -la
```

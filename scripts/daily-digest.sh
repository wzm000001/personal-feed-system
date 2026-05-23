#!/usr/bin/env zsh
# daily-digest.sh — v8 每日 AI Digest (codex 版,macOS launchd 触发)
#
# v8 关键改动 (相对 v7-claude-bobdong):
#   - 弃用 claude CLI(跟 bobdong.cn 不兼容,401 死路)
#   - 改用 codex CLI(走 ChatGPT 订阅,GPT-5.5 + xhigh reasoning)
#   - codex 是 shell-exec agent: Read=cat, Write=heredoc>file, WebFetch=curl, Edit=sed
#   - --dangerously-bypass-approvals-and-sandbox 让 codex 能写 vault + curl Discord
#   - 代理 7897(Clash 实际端口,不是 7892)
#
# 流程：
#   1) 加载环境 (HTTPS_PROXY=7897 + Discord webhook)
#   2) 健康检查 (codex CLI / 代理 / Discord webhook)
#   3) 调用 codex exec 跑 v7 daily-digest 流程(shell-exec 工具映射)
#   4) 日志写到 ~/.claude/logs/daily-digest-{YYYY-MM-DD}.log

set -e
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR="$HOME/.claude/logs"
LOG="$LOG_DIR/daily-digest-$TODAY.log"
mkdir -p "$LOG_DIR"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

log "=========================================="
log "Daily Digest v8 (codex) 启动 · $NOW"
log "=========================================="

# Step 1: 加载环境
log "Step 1: 加载环境"
[ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null || true
export PATH="$HOME/.local/bin:$PATH"
export LLM_WIKI_GLOBAL_DIR="${LLM_WIKI_GLOBAL_DIR:-$HOME/Documents/obsidian/bgggcontent}"

# 代理 7897(Clash 实际端口),给 codex 内部 wss + curl Discord/RSS
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7897}"
export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7897}"
export NO_PROXY="127.0.0.1,localhost,.local"
export no_proxy="$NO_PROXY"

# Discord webhook 来自 follow-builders/.env
if [ -f "$HOME/.follow-builders/.env" ]; then
  set -a
  source "$HOME/.follow-builders/.env"
  set +a
fi

# v8 注意: 不再 source proxy.env(那是给 claude CLI 用的 bobdong.cn 凭据)
# codex 走 ChatGPT 订阅,自动从 ~/.codex/auth.json 读
# 清掉 ANTHROPIC 相关 env,避免 codex 误判
unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL ANTHROPIC_MODEL 2>/dev/null || true

log "  LLM_WIKI_GLOBAL_DIR=$LLM_WIKI_GLOBAL_DIR"
log "  HTTPS_PROXY=$HTTPS_PROXY"
log "  DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL:0:50}..."

# Step 2: 健康检查
log "Step 2: 健康检查"

# codex CLI - 写死路径不用 which(避免 alias 在非交互 shell 看不见)
CODEX_BIN="$HOME/.local/bin/codex"
if [ ! -x "$CODEX_BIN" ]; then
  # fallback 试 alias 那个 wrapper
  CODEX_BIN="/path/to/your/codex/wrapper" # 可选 fallback,自己改
  if [ ! -x "$CODEX_BIN" ]; then
    log "❌ codex CLI 不可用 - 试过 ~/.local/bin/codex 和 codex-xigua 都找不到"
    exit 1
  fi
fi
log "  ✅ codex CLI ($CODEX_BIN)"

# codex 登录态
if [ ! -f "$HOME/.codex/auth.json" ]; then
  log "❌ codex 未登录,运行 'codex login' 配置 ChatGPT 订阅"
  exit 1
fi
log "  ✅ codex 已登录"

# 代理通不通
if ! nc -z -G 1 127.0.0.1 7897 2>/dev/null; then
  log "⚠️ 代理 7897 端口没监听 (Clash 可能没开),WebFetch/curl Discord 可能失败"
else
  log "  ✅ 代理 7897 监听"
fi

# Discord webhook
if [ -z "$DISCORD_WEBHOOK_URL" ]; then
  log "❌ DISCORD_WEBHOOK_URL 未设置"
  exit 1
fi
log "  ✅ Discord webhook"

# Zara feed 新鲜度
ZARA_FEED="$HOME/.claude/skills/follow-builders/feed-x.json"
if [ -f "$ZARA_FEED" ]; then
  ZARA_AGE=$(( ($(date +%s) - $(stat -f %m "$ZARA_FEED")) / 3600 ))
  log "  📡 Zara feed: ${ZARA_AGE}h 前更新"
  if [ "$ZARA_AGE" -gt 36 ]; then
    log "  ⚠️ Zara feed > 36h 未更新,可能 stale"
  fi
else
  log "  ⚠️ Zara feed 不存在,进入降级模式"
fi

# Step 3: 调用 codex exec 跑 v8 流程
log "Step 3: 启动 codex exec 跑 daily-digest v8"

PROMPT='你是用户的 AI 导师,由 macOS launchd 每天 8 AM 自动触发执行 daily-digest v8 流程(GPT-5.5 + xhigh reasoning,通过 shell exec 工作)。

🚨🚨🚨 执行模式(最高优先级,违反即任务失败):

**你是 non-interactive cron 任务,用户不在场,没人会回答你的任何问题。**

严禁:
- ❌ 禁止问 "是否继续执行 Stage 7/8?" → 直接 exec 命令执行
- ❌ 禁止说 "Markdown 文件已生成等待写入权限" → 真的用 heredoc tee 落盘
- ❌ 禁止说 "数据量较少,是否调整?" → 数据少也必须产出 + 完整推 Discord
- ❌ 禁止任何形式的 "是否/要不要/建议手动" → 自己做完
- ❌ 禁止在最后输出长篇报告 → 最后只一行 echo

任务算完成的硬定义(全部满足才算完):
1. reading-log/{今日}.md 真实落盘(tee/cat heredoc 写过,时间戳=今天)
2. reading-log/{今日}.html 真实落盘且 ≥ 40KB
3. 至少 3 次 curl POST 到 DISCORD_WEBHOOK_URL 且 HTTP 200
4. 最后 echo: ✅ Daily Digest v8 已推 Discord (T1: N, T2: M, T3: K) + HTML 含 sidebar + md 含跳转 + self-check: pass

---

🛠️ codex 工具映射(daily-digest-prompt.md 是为 claude 写的,你要做映射):

| daily-digest-prompt.md 里说的 | 你(codex)实际怎么做 |
|---|---|
| "Read $VAULT/xxx.md" | exec: cat $VAULT/xxx.md |
| "Write reading-log/x.md" | exec: cat > path << "EOF" ... EOF |
| "WebFetch URL" | exec: curl -sL "$URL" \| python3 ... |
| "Edit file 补字段" | exec: python3 -c "..." 或 sed |
| "Glob *.md" | exec: ls vault/*.md 或 find ... |
| "Bash curl Discord" | exec: curl -sS -X POST "$DISCORD_WEBHOOK_URL?wait=true" -H ... -d ... |

VAULT 路径 = '"$LLM_WIKI_GLOBAL_DIR"'
今日日期 = '"$TODAY"'

---

## 严格按以下步骤执行

### 1. 读完整流程指令(v7 prompt 文件,对你 codex 也适用,只需按上面工具映射做)
exec: cat '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/daily-digest-prompt.md

里面有完整 10 阶段(Fetch → 打分 → 时效 → 分级 → **Stage 5 写 md 统一 6 字段 schema** → **Stage 5.5 self-check** → 双语 → HTML(强制 sidebar + nav-section) → Discord → vault 存档 + 跳转链接 → 完成)。

### 2. 读 vault 三件套(v8 升级 · 立体认知)
exec:
  cat '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/user-profile.md            # 基础 + 当前真问题
  cat '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/vault-topics-summary.md    # 15 topics + 4 concepts 索引
  cat '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/recent-activity.md         # 近 14 天 vault 注意力热度
  cat '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/reading-feeds.md           # 90 信源池
  for f in '"$LLM_WIKI_GLOBAL_DIR"'/00-Wiki/feed-prompts/*.md; do cat "$f"; done

⚠️ Stage 5 引发思考(💭)必须 cite vault-topics-summary 里的具体 topic/concept 路径,不能只用 user-profile 的真问题。
⚠️ Stage 5 "这条在讲什么"段拆 3-5 段, 每段 ≤3 句, 中间穿插视觉, 禁止 300 字密集长段。
⚠️ Stage 3.5 信源多样性硬约束: Tier 1 必须跨 3+ 媒介(🎬视频+📱X+📰博客+🐙GitHub+🇨🇳中文圈), GitHub 最多 2 条。
⚠️ Stage 7 HTML 是"正片", 术语用 CSS+JS popup tooltip(不是 <abbr>), 40+ 词白名单都要 tooltip 化, metaphor 必须基于本条具体内容(禁止 default 模板).
⚠️ Stage 8 Discord 每块必须含 💎价值点 + 💭 vault cite + 📖去HTML看什么 + 🔗 链接, 严禁 default 文案如"建议放进 agent 工程知识链".
⚠️ Stage 11 跑完后必须重新生成 vault-topics-summary.md + recent-activity.md。

### 3. 读 Zara feed (本地 JSON 抓快,核心数据来源)
exec: cat ~/.claude/skills/follow-builders/feed-{x,podcasts,blogs}.json

### 4. 抓 RSS / WebFetch (reading-feeds.md 里列了 ~90 信源)
exec 多次 curl,失败的源跳过不崩。Tier S/A 信源(头部 25 builder)优先。

### 5. 价值打分(Primary×0.3 + Influence×0.4 + Recency×0.3),时效过滤(<30d 为主 + evergreen 白名单)

### 6. 3-tier 分级(参考 daily-digest-prompt.md Stage 4)

### 7. 写 reading-log/'"$TODAY"'.md (按 6 字段 schema,参考 prompt 里的 few-shot example)

每条 Tier 1/2/3 必须有 7 字段:
  ① 元数据(📅 时效 + 👤 作者)
  ② "这条在讲什么"段
  ③ 💎 价值点
  ④ 💭 引发的思考(必须 cite user-profile 具体字段,如 data-bp / agentic-systems-theory / AI 副业 / vault / Claude Code)
  ⑤ 📖 带着思考去读
  ⑥ 🎯 Quiz + 答案(用 <details> 折叠)
  ⑦ 🔗 链接

md frontmatter 后必须有一行可点击跳转:
[📖 查看 HTML 杂志(含目录)](./'"$TODAY"'.html)

### 8. self-check (Stage 5.5)
exec: cat reading-log/'"$TODAY"'.md, 然后对每条 record 验 7 字段,缺则用 python3 补字段(不要重写整个文件)

### 9. 写 reading-log/'"$TODAY"'.html
必须双栏 layout + <aside class="sidebar"> + Tier 1/2/3 三个 nav-section。参考 reading-log/2026-05-22.html 的 sidebar 实现(53KB 那版)。

### 10. 推 Discord (Stage 8)
分块 curl POST 到 $DISCORD_WEBHOOK_URL?wait=true,每块 < 1900 字符:
- Block 1: 头部(日期 + Tier 统计 + 提示有 HTML 杂志)
- Block 2..N: 每条 Tier 1 单独一块
- Block N+1: Tier 2 合并
- Block N+2: Tier 3 简版

每块 POST 后检查 HTTP 200,失败 retry 1 次。

### 11. 最后 echo 一行结果
✅ Daily Digest v8 已推 Discord (T1: N, T2: M, T3: K) + HTML 含 sidebar + md 含跳转 + self-check: pass

## 关键约束
- focus AI(跳过非 AI,如 sama 悼念推、政治、应酬)
- 双语(中文为主,关键术语和人名/产品名/公司名保留英文)
- 任何源失败降级不崩
- 你不被任何东西打断,一路 exec 到 echo 那行结束
- DISCORD_WEBHOOK_URL 已经在 env 里(你执行 echo $DISCORD_WEBHOOK_URL 能拿到)

立即开始执行。'

log "  开始执行 (codex GPT-5.5 + xhigh reasoning,预计 30-60 分钟)..."

# codex exec:
#   --dangerously-bypass-approvals-and-sandbox = cron 任务跳沙箱,允许写 vault + curl 外网
#   --skip-git-repo-check = 不在 git repo 也能跑
#   --cd $HOME = 在 home 目录跑,避免 cwd 限制
"$CODEX_BIN" exec \
  --dangerously-bypass-approvals-and-sandbox \
  --skip-git-repo-check \
  --cd "$HOME" \
  "$PROMPT" 2>&1 | tee -a "$LOG"
RC=$?

log "Step 4: 完成"
if [ $RC -eq 0 ]; then
  log "✅ Daily Digest v8 (codex) 成功"
else
  log "❌ Daily Digest v8 (codex) 失败 (rc=$RC),看上面日志"
fi

log "=========================================="
log "Daily Digest v8 (codex) 结束 · $(date +%H:%M:%S)"
log "=========================================="

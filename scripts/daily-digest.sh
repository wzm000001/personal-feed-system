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
  CODEX_BIN="/path/to/your/codex/wrapper" # 可选 fallback
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

# Step 3: 拆分两阶段调用 codex (v10 新增 wss 断线 retry)
# Phase 1: Stage 0-5 写 md (主流程, 30-60min, 容易断)
# Phase 2: Stage 5.6-11 写 extras+html+Discord+sync (短任务 5min)
# 两阶段之间产物自检, 失败 retry, 都失败通知用户人工

MD_PATH="$LLM_WIKI_GLOBAL_DIR/01-Sources/reading-log/$TODAY.md"
EXTRAS_PATH="$LLM_WIKI_GLOBAL_DIR/01-Sources/reading-log/$TODAY.extras.json"
HTML_PATH="$LLM_WIKI_GLOBAL_DIR/01-Sources/reading-log/$TODAY.html"
PROMPT_FILE="$LLM_WIKI_GLOBAL_DIR/00-Wiki/daily-digest-prompt.md"

verify_md_complete() {
  [ -f "$MD_PATH" ] || return 1
  local n=$(grep -c "^### " "$MD_PATH" 2>/dev/null)
  [ "$n" -ge 16 ]
}

verify_artifacts_complete() {
  [ -f "$MD_PATH" ] || return 1
  [ -f "$EXTRAS_PATH" ] || return 1
  [ -f "$HTML_PATH" ] || return 1
  local html_size=$(stat -f %z "$HTML_PATH" 2>/dev/null)
  [ "$html_size" -ge 50000 ]
}

notify_failure() {
  local stage="$1"
  local reason="$2"
  log "❌ $stage 失败: $reason"
  if [ -n "$DISCORD_WEBHOOK_URL" ]; then
    curl -sS -X POST "${DISCORD_WEBHOOK_URL}?wait=true" \
      -H "Content-Type: application/json" \
      -d "{\"content\":\"⚠️ daily-digest $TODAY $stage 失败: $reason. 需手动救场.\"}" >/dev/null 2>&1
  fi
}

PROMPT_PHASE1='你是用户的 AI 导师, 由 macOS launchd 每天 8 AM 自动触发, 现在是 daily-digest v10 的 **Phase 1 主流程**。

🚨 Phase 1 只做: Stage 0-5 写 reading-log/{date}.md (16 条 Tier 1/2/3, 7 字段完整)。
🚨 不做 Stage 5.6 (extras.json) / 7 (HTML) / 8 (Discord) / 11 — Phase 2 做这些。

执行步骤:
1. cat '"$PROMPT_FILE"' (读完整 spec)
2. 按 spec 跑 Stage 0-5:
   - Stage 0: 读 vault 三件套 (user-profile + vault-topics-summary + recent-activity)
   - Stage 1: 抓 90+ 信源 (Zara feed + RSS + WebFetch + 中文 KOL)
   - Stage 2: 价值打分
   - Stage 3: 时效过滤
   - Stage 3.5: 信源多样性硬约束 (Tier 1 跨 3+ 媒介)
   - Stage 4: 3-Tier 分级
   - Stage 5: 写 '"$MD_PATH"' (16 条全 7 字段 schema)
3. Stage 5.5: cat 自己写的 md 自检, 缺字段补
4. echo 一行: "✅ Phase 1 完成: md 16 条全字段"

严禁:
- ❌ 写 extras.json / 写 html / 推 Discord — 那是 Phase 2 的事
- ❌ 问 "是否继续" — non-interactive cron
- ❌ 数据少就跳过 — 必须产出 16 条'

PROMPT_PHASE2='你是 daily-digest v10 的 **Phase 2 收尾流程**。

🚨 Phase 1 已经写好了 '"$MD_PATH"' (16 条基础内容)。你的工作只剩:

执行步骤:
1. cat '"$MD_PATH"' 看 16 条 (Tier 1/2/3) 的标题 + 讲什么 + 价值点
2. 写 '"$EXTRAS_PATH"': 严格 JSON, 16 条 entries (t1-1 t1-2 ... t3-5), 每条:
   {
     "metaphor": "独特生活/工程比喻 30-80 字, 必须基于本条具体事实(产品/数字/场景), 禁止 default 模板",
     "features": [
       {"emoji": "📊", "title": "≤8 字短标题", "desc": "15-30 字解释"},
       {"emoji": "🔧", "title": "...", "desc": "..."}
     ],
     "flow": ["节点1 ≤8字", "节点2", "节点3", "节点4"]
   }
   16 条都要写, features 4-6 个, flow 4-5 节点
3. 写完后 python3 -m json.tool 验证 JSON 合法
4. exec python3 '"$HOME"'/.claude/scripts/render-html.py '"$MD_PATH"' '"$HTML_PATH"'
5. 验证 stat -f %z '"$HTML_PATH"' ≥ 50000 bytes
6. 分块 curl POST $DISCORD_WEBHOOK_URL?wait=true (预告片模式, 7 块, 详见 '"$PROMPT_FILE"' Stage 8)
7. Stage 11: 重新生成 $VAULT/00-Wiki/vault-topics-summary.md 和 recent-activity.md
8. 最后 echo: "✅ Daily Digest v10 已推 Discord (T1: 5, T2: 6, T3: 5) + HTML 含 sidebar + md 含跳转 + extras 齐全 + self-check: pass"

严禁:
- ❌ 重新抓信源 / 重新打分 / 重新分级 — md 已经写好, 你只补 extras + html + Discord
- ❌ 问 "是否继续" — 直接做完'

# === Phase 1: 主流程 ===
for attempt in 1 2; do
  log "Step 3 Phase 1 (主流程, 第 $attempt 次): codex 写 md"
  log "  开始执行 (codex GPT-5.5 + xhigh reasoning, 预计 30-60 分钟)..."
  "$CODEX_BIN" exec \
    --dangerously-bypass-approvals-and-sandbox \
    --skip-git-repo-check \
    --cd "$HOME" \
    "$PROMPT_PHASE1" 2>&1 | tee -a "$LOG"
  if verify_md_complete; then
    log "✅ Phase 1 完成 (第 $attempt 次): md 16 条齐全"
    break
  fi
  log "⚠️ Phase 1 第 $attempt 次 md 不完整, retry"
  if [ "$attempt" -eq 2 ]; then
    notify_failure "Phase 1" "md 两次都没写完整"
    exit 1
  fi
done

# === Phase 2: 收尾 ===
for attempt in 1 2 3; do
  log "Step 3 Phase 2 (收尾, 第 $attempt 次): codex 写 extras + html + Discord"
  log "  开始执行 (预计 3-10 分钟, 短任务)..."
  "$CODEX_BIN" exec \
    --dangerously-bypass-approvals-and-sandbox \
    --skip-git-repo-check \
    --cd "$HOME" \
    "$PROMPT_PHASE2" 2>&1 | tee -a "$LOG"
  if verify_artifacts_complete; then
    log "✅ Phase 2 完成 (第 $attempt 次): extras + html + Discord 全齐"
    break
  fi
  log "⚠️ Phase 2 第 $attempt 次产物不完整, retry"
  if [ "$attempt" -eq 3 ]; then
    notify_failure "Phase 2" "extras/html 三次都没生成完整 — 已有 md 在 $MD_PATH, 你可手动调 render.py"
    RC=2
  fi
done

[ -z "$RC" ] && RC=0

log "Step 4: 完成"
if [ $RC -eq 0 ]; then
  log "✅ Daily Digest v8 (codex) 成功"
else
  log "❌ Daily Digest v8 (codex) 失败 (rc=$RC),看上面日志"
fi

log "=========================================="
log "Daily Digest v8 (codex) 结束 · $(date +%H:%M:%S)"
log "=========================================="

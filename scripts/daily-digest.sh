#!/usr/bin/env zsh
# daily-digest.sh — v4 每日 AI Digest（macOS launchd 触发）
#
# 流程：
#   1) 加载环境（.zshrc + .follow-builders/.env）
#   2) 健康检查（claude CLI / Zara feed / Discord webhook）
#   3) 调用 `claude -p` 启动 LLM session 跑 v4 daily-digest 流程
#   4) 日志写到 ~/.claude/logs/daily-digest-{YYYY-MM-DD}.log

set -e
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR="$HOME/.claude/logs"
LOG="$LOG_DIR/daily-digest-$TODAY.log"
mkdir -p "$LOG_DIR"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

log "=========================================="
log "Daily Digest v4 启动 · $NOW"
log "=========================================="

# Step 1: 加载环境
log "Step 1: 加载环境"
[ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null || true
export PATH="$HOME/.local/bin:$PATH"
export LLM_WIKI_GLOBAL_DIR="${LLM_WIKI_GLOBAL_DIR:-$HOME/Documents/obsidian/bgggcontent}"

if [ -f "$HOME/.follow-builders/.env" ]; then
  set -a
  source "$HOME/.follow-builders/.env"
  set +a
fi

log "  LLM_WIKI_GLOBAL_DIR=$LLM_WIKI_GLOBAL_DIR"
log "  DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL:0:50}..."

# Step 2: 健康检查
log "Step 2: 健康检查"
CLAUDE_BIN="$HOME/.local/bin/claude"
if [ ! -x "$CLAUDE_BIN" ]; then
  log "❌ claude CLI 不可用: $CLAUDE_BIN"
  exit 1
fi
log "  ✅ claude CLI"

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
    log "  ⚠️ Zara feed > 36h 未更新，可能 stale"
  fi
else
  log "  ⚠️ Zara feed 不存在，进入降级模式"
fi

# Step 3: 调用 claude CLI 执行 v4 流程
log "Step 3: 启动 claude -p 跑 daily-digest v4"

PROMPT='你是用户的 AI 导师，由 macOS launchd 每天 8 AM 自动触发执行 daily-digest v4 流程。

## 严格按以下步骤执行

### 1. 读完整流程指令
Read $HOME/Documents/obsidian/bgggcontent/00-Wiki/daily-digest-prompt.md

里面有完整 8 阶段（Fetch → 打分 → 分级 → Remix → 双语 → Discord 推送 → vault 存档 → 完成）。

### 2. 读信源池
Read $HOME/Documents/obsidian/bgggcontent/00-Wiki/reading-feeds.md

约 90 信源，分 Tier S/A/B/C/D。

### 3. 读 prompts 模板
Glob 然后 Read $HOME/Documents/obsidian/bgggcontent/00-Wiki/feed-prompts/*.md

5 个模块化 prompt。

### 4. 严格按 daily-digest-prompt.md 的 Stage 1-8 执行

## 环境
- DISCORD_WEBHOOK_URL 已 set（来自 ~/.follow-builders/.env）
- LLM_WIKI_GLOBAL_DIR=$HOME/Documents/obsidian/bgggcontent
- 工具: curl, gh, python3, jq, WebFetch, Bash
- Zara feed: ~/.claude/skills/follow-builders/feed-{x,podcasts,blogs}.json

## 关键约束
- focus AI（不扯非 AI）
- 双语（英文 + 中文翻译，关键术语保留英文）
- 3-tier 分级（Value = Primary×0.3 + Influence×0.4 + Recency×0.3）
- 时效 < 30d 为主 + evergreen 白名单每周 1 篇 rotate
- 7 天去重（查 reading-log/）
- Tier 1+2 推 Discord，Tier 3 仅 vault
- 任何源失败降级不崩
- 不在 chat 输出完整 digest（推 Discord + 写 vault 即可）
- chat 最后只 echo 一行: "✅ Daily Digest 已推 Discord (Tier 1: N, Tier 2: M, Tier 3 归档 K)"

## 失败处理
- Discord 推送失败 → 重试 1 次，仍失败 echo 错误
- 个别源抓取失败 → 跳过该源继续
- 完全失败 → echo 错误，不写 vault

立即开始执行。'

log "  开始执行（预计 2-5 分钟）..."
"$CLAUDE_BIN" -p "$PROMPT" --output-format=text 2>&1 | tee -a "$LOG"
RC=$?

log "Step 4: 完成"
if [ $RC -eq 0 ]; then
  log "✅ Daily Digest v4 成功"
else
  log "❌ Daily Digest v4 失败 (rc=$RC)，看上面日志"
fi

log "=========================================="
log "Daily Digest v4 结束 · $(date +%H:%M:%S)"
log "=========================================="

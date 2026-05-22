#!/usr/bin/env zsh
# feed-daily.sh — 每日 AI 阅读推送
# Usage: 由 launchd 每日早 8 点触发，或手动跑 `~/.claude/scripts/feed-daily.sh`
#
# 流程：
#   1) source ~/.zshrc 拿环境变量（WEREAD_API_KEY、LLM_WIKI_GLOBAL_DIR 等）
#   2) 调用 `claude -p "/feed --push"` 生成 reading-log + 推送
#   3) 日志写到 ~/.claude/logs/feed-daily-{YYYY-MM-DD}.log
#   4) 失败时 fallback：用 Zara feed-x.json + lark-cli 做简化推送

set -e
TODAY=$(date +%Y-%m-%d)
NOW=$(date +"%Y-%m-%d %H:%M:%S")
LOG_DIR="$HOME/.claude/logs"
LOG_FILE="$LOG_DIR/feed-daily-$TODAY.log"
mkdir -p "$LOG_DIR"

# 日志辅助函数
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }

log "=========================================="
log "Feed Daily 启动 · $NOW"
log "=========================================="

# Step 1: 加载环境变量
log "Step 1: 加载 ~/.zshrc"
if [ -f "$HOME/.zshrc" ]; then
  # shellcheck disable=SC1091
  source "$HOME/.zshrc" 2>/dev/null || true
fi

# 设置默认值（防止 zshrc 没加载）
export PATH="$HOME/.local/bin:$PATH"
export LLM_WIKI_GLOBAL_DIR="${LLM_WIKI_GLOBAL_DIR:-$HOME/Documents/obsidian/bgggcontent}"

log "  PATH=$PATH"
log "  LLM_WIKI_GLOBAL_DIR=$LLM_WIKI_GLOBAL_DIR"
log "  WEREAD_API_KEY=${WEREAD_API_KEY:0:8}..."

# Step 2: 健康检查
log "Step 2: 健康检查"
CLAUDE_BIN="$HOME/.local/bin/claude"
LARK_BIN="$HOME/.local/bin/lark-cli"

if [ ! -x "$CLAUDE_BIN" ]; then
  log "❌ claude CLI 不可用: $CLAUDE_BIN"
  exit 1
fi
log "  ✅ claude CLI: $CLAUDE_BIN"

if [ ! -x "$LARK_BIN" ]; then
  log "⚠️  lark-cli 不可用: $LARK_BIN (推送降级到邮件)"
fi
log "  ✅ lark-cli: $LARK_BIN"

# 检查 Zara feed 新鲜度
ZARA_FEED="$HOME/.claude/skills/follow-builders/feed-x.json"
if [ -f "$ZARA_FEED" ]; then
  ZARA_AGE=$(( ($(date +%s) - $(stat -f %m "$ZARA_FEED")) / 3600 ))
  log "  📡 Zara feed-x.json 年龄: ${ZARA_AGE} 小时"
  if [ "$ZARA_AGE" -gt 36 ]; then
    log "  ⚠️  Zara feed 超过 36 小时未更新，可能 stale"
  fi
fi

# Step 3: 调用 /feed 命令
log "Step 3: 调用 claude -p '/feed --push'"

PROMPT='/feed --push'
OUTPUT=$("$CLAUDE_BIN" -p "$PROMPT" --output-format=text 2>&1 | tee -a "$LOG_FILE")
RC=$?

if [ $RC -ne 0 ]; then
  log "❌ /feed 调用失败 (rc=$RC)，进入 fallback"

  # Fallback: 用 Zara feed + lark-cli 做简化推送
  log "Fallback: 简化版推送"

  if [ -f "$ZARA_FEED" ] && [ -x "$LARK_BIN" ]; then
    SUMMARY=$(python3 <<'EOF'
import json, os
feed = json.load(open(os.path.expanduser('~/.claude/skills/follow-builders/feed-x.json')))
lines = [f"☀️ 早安，今日 AI Builders Digest（{feed['generatedAt'][:10]}）", ""]
lines.append(f"📡 来源：Zara 中心化 feed · {len(feed['x'])} builder · {sum(len(b['tweets']) for b in feed['x'])} 推文（24h 窗口）")
lines.append("")
lines.append("最新推文 Top 5（按 likes 排序）：")
all_tweets = []
for b in feed['x']:
    for t in b['tweets']:
        t['builder'] = b['name']
        all_tweets.append(t)
top = sorted(all_tweets, key=lambda t: t.get('likes', 0), reverse=True)[:5]
for i, t in enumerate(top, 1):
    text = t.get('text', '')[:120].replace('\n', ' ')
    lines.append(f"{i}. **{t['builder']}** ({t.get('likes',0)} ❤️)")
    lines.append(f"   {text}")
    lines.append(f"   🔗 {t.get('url','')}")
    lines.append("")
lines.append("(完整 /feed 流程失败，这是 fallback 输出)")
print('\n'.join(lines))
EOF
)
    echo "$SUMMARY" > /tmp/feed-fallback.md
    "$LARK_BIN" im send --to me --message-file /tmp/feed-fallback.md 2>&1 | tee -a "$LOG_FILE" || true
  fi
  exit 0
fi

log "Step 4: 完成"
log "Output preview:"
echo "$OUTPUT" | head -20 | tee -a "$LOG_FILE"

log "=========================================="
log "Feed Daily 结束 · $(date +%H:%M:%S)"
log "=========================================="

# 安装指南 · v6

> 部署 personal-feed-system v6（AI 导师模式 + 用户档案 + 可视化 HTML + Discord 推送）到你的 macOS。

## 前提

- **macOS**（Linux 部分可用，launchd 部分要换成 systemd timer，本指南不展开）
- **Claude Code** 已装且可用（CLI 路径通常是 `~/.local/bin/claude`）
- **Obsidian vault**（任意路径）
- **Discord 账号**（创建一个 server + channel + webhook）

---

## 总体架构（v6）

```
launchd 每天 8 AM 触发
    ↓
~/.claude/scripts/daily-digest.sh
    ↓
启动 claude -p 跑 v6 完整流程：
  Stage 0: 读 user-profile.md（持续了解用户）
  Stage 1: 抓 92 信源（Zara feed-x.json + 88 RSS/Atom/WebFetch）
  Stage 2: Value 打分（Primary × 0.3 + Influence × 0.4 + Recency × 0.3）
  Stage 3: 时效硬限制 < 30 天 + Evergreen 白名单 weekly rotate
  Stage 4: 3-tier 分级（都有价值，区别在投入时间）
  Stage 5-6: 总结写法 + 中文为主 + 关键术语英文
  Stage 7: HTML 杂志生成（codebase-to-course 风格）
  Stage 8: Discord 推送（webhook ?wait=true 顺序保证）
  Stage 9: vault 存档 reading-log/{date}.{md,html}
  Stage 10: 主动更新 user-profile.md
```

---

## Step 1: 克隆 repo

```zsh
git clone https://github.com/wzm000001/personal-feed-system.git ~/personal-feed-system
cd ~/personal-feed-system
```

## Step 2: 设置 vault 路径

把你 Obsidian vault 的根路径加到 `~/.zshrc`：

```zsh
echo "export LLM_WIKI_GLOBAL_DIR=\"\$HOME/Documents/<your-vault-name>\"" >> ~/.zshrc
source ~/.zshrc
echo "$LLM_WIKI_GLOBAL_DIR"   # 应该输出你 vault 的绝对路径
```

## Step 3: 复制配置文件到 vault

```zsh
mkdir -p "$LLM_WIKI_GLOBAL_DIR/00-Wiki/feed-prompts"
mkdir -p "$LLM_WIKI_GLOBAL_DIR/01-Sources/reading-log"

# 信源池（92 源全集）
cp reading-feeds.md "$LLM_WIKI_GLOBAL_DIR/00-Wiki/"

# 流程指令（v6 完整版）
cp daily-digest-prompt.md "$LLM_WIKI_GLOBAL_DIR/00-Wiki/"

# 用户档案模板（v6 新增 · 必读）
cp user-profile.md "$LLM_WIKI_GLOBAL_DIR/00-Wiki/"

# 5 个模块化 prompt（来自 Zara follow-builders）
cp feed-prompts/*.md "$LLM_WIKI_GLOBAL_DIR/00-Wiki/feed-prompts/"
```

## Step 4: 个性化 user-profile.md ⭐ v6 关键

打开 `$VAULT/00-Wiki/user-profile.md`，**改成你自己的信息**：

```
# 必改字段：
- 基础信息（姓名、工作、当前项目、设备、时区）
- AI 兴趣（你关心 AI 的哪些方面、优先级）
- 跳过的内容（你不想看的）
- 当前真问题（3-5 条，你近期投入的事）
- 内容偏好（语言、篇幅、媒介）
- 技术栈（已用工具、技能栈）
- Vault 状态（你的 topic 列表 + coverage）
```

**这个文件是 AI 导师的"长期记忆"**。每次定时推送前 AI 必读，所有"引发的思考"都会 cite 这里的字段。**写得越详细越准确，推荐就越精准**。

## Step 5: 装可选依赖

### 5a. Zara follow-builders（强烈推荐 · 提供 25 builder + 6 播客的中心化 feed）

```zsh
git clone https://github.com/zarazhangrui/follow-builders.git ~/.claude/skills/follow-builders
cd ~/.claude/skills/follow-builders/scripts && npm install
```

确认 feed 文件存在：
```zsh
ls ~/.claude/skills/follow-builders/feed-x.json
```

### 5b. yt-dlp（YouTube 字幕，可选 · 你想看视频精华时用）

```zsh
mkdir -p ~/.local/bin
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o ~/.local/bin/yt-dlp
chmod +x ~/.local/bin/yt-dlp
```

### 5c. 微信读书 skill（可选 · v6 焦点在 AI 后用得少）

```zsh
curl -sSL https://cdn.weread.qq.com/skills/weread-skills.zip -o /tmp/weread.zip
unzip /tmp/weread.zip -d ~/.claude/skills/
echo "export WEREAD_API_KEY=wrk-xxxxx" >> ~/.zshrc   # 替换成你自己的 key
```

### 5d. codebase-to-course skill（推荐 · HTML 杂志参考）

```zsh
git clone https://github.com/zarazhangrui/codebase-to-course.git ~/.claude/skills/codebase-to-course
```

## Step 6: 配置 Discord webhook ⭐ v6 推送通道

### 6a. 创建 Discord webhook

1. 打开 Discord（桌面 / 网页）
2. 选一个 server（或新建一个，如 "AI Digest"）
3. 选 channel（或新建 `#daily-feed`）
4. 频道齿轮 ⚙️ → **Integrations → Webhooks → New Webhook**
5. 命名 "AI 导师"，**Copy Webhook URL**

⚠️ **Webhook URL 等于密码**：任何拿到的人都能往你 channel 发消息。**不要贴到任何公开地方**。

### 6b. 保存到本地

```zsh
mkdir -p ~/.follow-builders
cat > ~/.follow-builders/.env << EOF
DISCORD_WEBHOOK_URL=粘贴你的URL到这里
EOF
chmod 600 ~/.follow-builders/.env   # 只有你能读
```

### 6c. 验证 webhook 可用

```zsh
source ~/.follow-builders/.env
curl -s -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"username":"AI 导师","content":"✅ Webhook 连接测试成功"}' \
  -w "\nHTTP: %{http_code}\n"
```

返回 `HTTP: 204` 表示成功 + Discord channel 应能看到"连接测试成功"消息。

## Step 7: 复制脚本 + launchd 定时器

### 7a. 复制脚本

```zsh
mkdir -p ~/.claude/scripts ~/.claude/logs
cp scripts/daily-digest.sh ~/.claude/scripts/daily-digest.sh
chmod +x ~/.claude/scripts/daily-digest.sh
```

### 7b. 配置 launchd plist

模板里的占位符替换为你的路径 + 起个 unique label：

```zsh
sed -e "s|\$HOME|$HOME|g" \
    -e "s|com.example|com.<your-id>|g" \
    LaunchAgents/com.example.daily-digest.plist \
    > ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist
```

（建议 `<your-id>` 用你的 GitHub username 或姓名拼音）

验证 plist 格式：
```zsh
plutil -lint ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist
# 应该输出: OK
```

### 7c. 启用 launchd

```zsh
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist
```

**无回显是正常的**（macOS 26 launchctl bootstrap 静默成功）。

### 7d. 验证 job 已注册

```zsh
launchctl list | grep daily-digest
```

应该看到一行类似：`-  0  com.<your-id>.daily-digest`
- `-` = PID（当前没运行，对的）
- `0` = 上次退出码（健康）

### 7e. 立即测试一次（推荐 · 不等明早）

```zsh
launchctl kickstart gui/$(id -u)/com.<your-id>.daily-digest
```

另开 terminal 跟踪日志：

```zsh
tail -f ~/.claude/logs/daily-digest-$(date +%Y-%m-%d).log
```

预计 **3-6 分钟** 完成。结束后：

- ✅ Discord channel 收到当日 v6 推送（含 Tier 1 完整深度 + Quiz + Tier 2 + Tier 3）
- ✅ `$VAULT/01-Sources/reading-log/YYYY-MM-DD.md` 已写
- ✅ `$VAULT/01-Sources/reading-log/YYYY-MM-DD.html` 已生成
- ✅ `$VAULT/00-Wiki/user-profile.md` 可能被 AI 主动更新（如果今天 PROFILE 信号有新主题）

---

## 维护命令

| 操作 | 命令 |
|---|---|
| **查看 job 是否注册** | `launchctl list \| grep daily-digest` |
| **立即手动触发** | `launchctl kickstart gui/$(id -u)/com.<your-id>.daily-digest` |
| **看今天日志** | `tail -50 ~/.claude/logs/daily-digest-$(date +%Y-%m-%d).log` |
| **看 launchd 错误** | `tail -50 ~/.claude/logs/daily-digest-launchd.err` |
| **禁用** | `launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist` |
| **重新启用** | `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist` |
| **改触发时间** | 编辑 plist 的 `<Hour>` / `<Minute>`，bootout → bootstrap |
| **看 system log** | `log show --predicate 'subsystem == "com.apple.xpc.launchd"' --last 1h \| grep daily-digest` |

> **关于 `launchctl print`**：macOS 26 简化了输出，**不再显示 `next launch` 字段**。但 `state = not running` + `calendarinterval` stream 存在 = 正在等待触发，是正常的。

---

## 故障排查

### 1. 立即测试时 claude CLI 报错

```zsh
# 手动测一下 claude CLI 是否可用
~/.local/bin/claude -p "say hello" --output-format=text
```

如果失败：
- 确认 Claude Code 已登录（运行 `claude` 看是否能开对话）
- 确认 `~/.local/bin` 在 `PATH`：`echo $PATH | grep .local/bin`

### 2. Discord 推送失败（log 显示 HTTP 4xx）

```zsh
# 检查 webhook URL 是否正确加载
source ~/.follow-builders/.env
echo "${DISCORD_WEBHOOK_URL:0:50}..."   # 应该输出 https://discord.com/api/webhooks/... 开头
```

- 如果空 → 检查 `~/.follow-builders/.env` 文件内容 + 权限
- HTTP 401/404 → URL 错或被 Discord 删除，重新创建 webhook
- HTTP 400 "Must be 2000 or fewer" → 内容超长，但 v6 已用分块发送，不应触发

### 3. Zara feed 文件不存在

```zsh
ls ~/.claude/skills/follow-builders/feed-x.json
```

如果没有：
```zsh
cd ~/.claude/skills/follow-builders
git pull   # Zara 每天更新
```

如果是首次安装：在 Claude Code 里跑一次 follow-builders skill 的 onboarding。

### 4. 用户档案没被读到

```zsh
ls $LLM_WIKI_GLOBAL_DIR/00-Wiki/user-profile.md
```

如果路径错：检查 `LLM_WIKI_GLOBAL_DIR` 环境变量是否对（`echo $LLM_WIKI_GLOBAL_DIR`）。

### 5. 每天 8 AM 没自动触发

```zsh
# job 还在不？
launchctl list | grep daily-digest

# 看 launchd 错误
tail -30 ~/.claude/logs/daily-digest-launchd.err

# 看脚本日志（如果触发过）
ls -lt ~/.claude/logs/daily-digest-*.log | head -3
```

常见原因：
- 电脑 8 AM 在睡眠 → launchd 会在唤醒后立即补跑
- Claude Code 没登录 → claude CLI 启动失败，看 log
- macOS 升级后 launchd 权限被重置 → bootout + bootstrap 重启 job

---

## 自定义

### 改信源池
编辑 `$VAULT/00-Wiki/reading-feeds.md`。下次定时推送自动用新版（不需要重启 launchd）。

### 改摘要风格
编辑 `$VAULT/00-Wiki/feed-prompts/*.md`。下次自动生效。

### 改推送时间
编辑 `~/Library/LaunchAgents/com.<your-id>.daily-digest.plist` 的 `<Hour>`/`<Minute>`，然后：
```zsh
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.daily-digest.plist
```

### 改 user-profile（当你工作变化时）
直接编辑 `$VAULT/00-Wiki/user-profile.md`。下次推送的"引发的思考"会基于新档案。

### 改 Discord channel
1. 在 Discord 创建新 webhook（旧的可以删）
2. 替换 `~/.follow-builders/.env` 的 `DISCORD_WEBHOOK_URL`
3. 不需要重启 launchd（脚本每次读 env）

---

## 关键文件清单（v6 部署后）

```
~/.claude/scripts/daily-digest.sh                     # launchd 触发的脚本
~/Library/LaunchAgents/com.<id>.daily-digest.plist    # launchd 配置
~/.follow-builders/.env                               # Discord webhook URL (600 权限)
~/.claude/logs/daily-digest-*.log                     # 每日运行日志
~/.claude/skills/follow-builders/                     # Zara 中心化 feed
$VAULT/00-Wiki/user-profile.md                        # ⭐ 用户档案（必读）
$VAULT/00-Wiki/daily-digest-prompt.md                 # v6 完整流程指令
$VAULT/00-Wiki/reading-feeds.md                       # 92 信源池
$VAULT/00-Wiki/feed-prompts/*.md                      # 5 个 prompt 模板
$VAULT/01-Sources/reading-log/YYYY-MM-DD.md           # 每日 markdown
$VAULT/01-Sources/reading-log/YYYY-MM-DD.html         # 每日 HTML 杂志
```

---

## 下一步

部署完成后建议：

1. **跑 1-2 次 `launchctl kickstart`** 立即测试，看推送效果
2. **去 Discord 看推送**，确认 Tier 1/2/3 都到 + 顺序对
3. **打开 `reading-log/*.html`** 看可视化杂志（Group Chat / SVG 流程图 / Quiz 折叠）
4. **每周 review user-profile.md** —— AI 主动更新的 "当前真问题" 节是否准确，不准就直接改
5. **每月 review reading-feeds.md** —— 信源是否需要调整（删死链 / 加新源）

---

## License

MIT

# 安装指南

## 前提

- macOS（Linux 也行，launchd 部分要换成 systemd timer）
- Claude Code 已装且可用（CLI: `~/.local/bin/claude` 或 `claude`）
- Obsidian vault（任意路径）
- 一个 GitHub 账号（如果你要 fork 本仓库）

## Step 1: 克隆这个 repo

```zsh
git clone https://github.com/<your-username>/personal-feed-system.git ~/personal-feed-system
cd ~/personal-feed-system
```

## Step 2: 设置 vault 路径环境变量

把你 Obsidian vault 的根路径加进 `~/.zshrc`：

```zsh
echo 'export LLM_WIKI_GLOBAL_DIR=~/Documents/<your-vault>' >> ~/.zshrc
source ~/.zshrc
```

## Step 3: 复制 slash command 到 Claude Code

```zsh
cp commands/feed.md ~/.claude/commands/feed.md
```

**重要**：复制后**重启 Claude Code** 才能识别新命令（启动时扫描，运行时不重扫）。

## Step 4: 复制信源池到 vault

```zsh
mkdir -p $LLM_WIKI_GLOBAL_DIR/00-Wiki
cp reading-feeds.md $LLM_WIKI_GLOBAL_DIR/00-Wiki/reading-feeds.md
```

## Step 5: 复制 prompt 模板到 vault

```zsh
mkdir -p $LLM_WIKI_GLOBAL_DIR/00-Wiki/feed-prompts
cp feed-prompts/*.md $LLM_WIKI_GLOBAL_DIR/00-Wiki/feed-prompts/
```

## Step 6: 装可选依赖

### Zara follow-builders（强烈推荐）

```zsh
git clone https://github.com/zarazhangrui/follow-builders.git ~/.claude/skills/follow-builders
cd ~/.claude/skills/follow-builders/scripts && npm install
```

### yt-dlp（YouTube 字幕，可选）

```zsh
mkdir -p ~/.local/bin
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos -o ~/.local/bin/yt-dlp
chmod +x ~/.local/bin/yt-dlp
```

### 微信读书 skill（可选）

```zsh
curl -sSL https://cdn.weread.qq.com/skills/weread-skills.zip -o /tmp/weread.zip
unzip /tmp/weread.zip -d ~/.claude/skills/
# 然后申请 API key 加到 ~/.zshrc：export WEREAD_API_KEY=wrk-xxxxx
```

### 飞书 lark-cli（推送依赖）

按 [lark-cli 官方安装文档](https://github.com/larksuite/lark-cli) 配。装完后：

```zsh
lark auth login
```

## Step 7: 测试 /feed 命令

打开 Claude Code，输入：

```
/feed
```

应该看到 8 信号源扫描 + 推荐输出，写入 `$VAULT/01-Sources/reading-log/{YYYY-MM-DD}.md`。

如果命令未识别，**重启 Claude Code 一次**（命令是启动时加载）。

## Step 8: 启用每日定时推送（可选）

### 配置脚本路径

```zsh
mkdir -p ~/.claude/scripts ~/.claude/logs
cp scripts/feed-daily.sh ~/.claude/scripts/feed-daily.sh
chmod +x ~/.claude/scripts/feed-daily.sh
```

### 配置 launchd

把 `LaunchAgents/com.example.feed-daily.plist` 里的占位符替换为你的路径：

```zsh
sed -e "s|\\\$HOME|$HOME|g" \
    -e "s|com.example|com.<your-id>|g" \
    LaunchAgents/com.example.feed-daily.plist \
    > ~/Library/LaunchAgents/com.<your-id>.feed-daily.plist
```

### 启用

```zsh
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.feed-daily.plist
```

### 立即测试一次

```zsh
launchctl kickstart gui/$(id -u)/com.<your-id>.feed-daily
tail -f ~/.claude/logs/feed-daily-$(date +%Y-%m-%d).log
```

### 禁用 / 修改时间

```zsh
# 禁用
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.<your-id>.feed-daily.plist

# 修改触发时间：编辑 plist 的 <Hour>/<Minute>，然后 bootout + bootstrap

# 查看下次触发时间
launchctl print gui/$(id -u)/com.<your-id>.feed-daily | grep -A 3 "next launch"
```

## 故障排查

### `/feed isn't a recognized command`

Claude Code 是启动时扫描 `~/.claude/commands/`。改完文件**必须重启 Claude Code**。

### Zara feed 文件不存在

确认你装了 follow-builders skill：
```zsh
ls ~/.claude/skills/follow-builders/feed-x.json
```

如果没有，跑一次它的 onboarding（在 Claude Code 里 `/follow-builders` 或自然语言触发）。

### 每日推送没跑

```zsh
# 查 launchd 是否注册
launchctl list | grep feed-daily

# 看日志
tail -50 ~/.claude/logs/feed-daily-$(date +%Y-%m-%d).log
tail -50 ~/.claude/logs/feed-daily-launchd.err
```

### lark-cli 失败

确认 `lark auth login` 已配。或者改用 `lark-mail` 推到邮箱。

## 自定义

### 改信源池

编辑 `$VAULT/00-Wiki/reading-feeds.md`，按 `# tag` 添加新源。
不需要重启 Claude Code，每次 `/feed` 都重新读这个文件。

### 改摘要风格

编辑 `$VAULT/00-Wiki/feed-prompts/summarize-*.md`。
下次 `/feed` 立刻生效。

### 改触发时间

编辑 plist 的 `<Hour>` / `<Minute>`，bootout + bootstrap 重启 launchd。

### 加新媒介

在 `commands/feed.md` 的 Stage 4 路径表加一行，定义抓取方式。

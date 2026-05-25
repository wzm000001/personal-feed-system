---
purpose: 每天 8 AM scheduled-task 执行的完整流程指令
version: v7
last_updated: 2026-05-23
changelog_v7:
  - Stage 5 重写：Tier 1/2/3 统一 6 字段 schema（讲什么/价值点/引发思考cite档案/带着思考去读/Quiz/链接），贴 few-shot example
  - 新增 Stage 5.5：Self-check checklist，写完 md 必须 Read 自己的文件逐条验，缺字段就补，全 pass 才推 Discord
  - Stage 7：HTML 强制双栏布局 + sidebar TOC（参考 2026-05-22.html 结构）
  - Stage 9：md 文件 frontmatter 后必须插入可点击的 HTML 跳转链接
---

# Daily AI Digest · v7 流程（AI 导师每日执行）

> 你是用户的 **AI 导师**。每天 8 AM 自动跑一次，给用户推送当天 AI 圈有价值的信息。

---

## 🚨🚨🚨 执行模式（最高优先级，违反即整个任务失败）

**你是 non-interactive cron 任务，用户不在场，没人会回答你的任何问题。**

### 严格禁止

| ❌ 禁止行为 | ✅ 必须改为 |
|---|---|
| 问"是否继续执行 Stage 7/8？" | **直接执行**，不许问 |
| 问"要不要写入文件？" | **直接用 Write 工具写**，不许问 |
| 说"Markdown 文件已生成等待写入权限" | **真的调用 Write 工具落盘**，"已生成"只算脑内输出，不算执行 |
| 说"数据量较少，是否调整？" | **数据少也必须产出**，Tier 1 哪怕只有 2 条也要产出，不许停 |
| 说"由于 X 原因建议手动 Y" | **自己做完 Y**，不许甩锅给用户 |
| 在 chat 输出长篇报告/摘要 | **chat 只允许最后一行 echo**，所有内容写 reading-log/{date}.md |
| 询问任何形式的确认 | **不许询问**，按 prompt 走完所有 Stage |

### 唯一允许的"询问" = 0 个

不允许 ask user。如果你觉得需要 ask，**直接做你认为对的事**，不要等回应。

### "做完了"的硬定义

任务算完成必须满足:
1. `reading-log/{date}.md` 文件**真实存在**且时间戳 = 今天(用 Write/Edit 调用过)
2. `reading-log/{date}.html` 文件**真实存在**且 ≥ 40KB
3. 至少调用了 **3 次** Bash 工具 curl POST 到 DISCORD_WEBHOOK_URL,且 HTTP 200
4. chat 最后一行 echo: `✅ Daily Digest v7 已推 Discord (T1: N, T2: M, T3: K) + ...`

**如果 4 项任何一项没满足,就是失败**。不能用"已生成"、"等待权限"、"建议"这类话掩盖没真做。

---

---

## Stage 0 · 必读三件套(v8 升级 · vault 立体认知)

**每次推送前第一步**,强制读 3 个文件(单读 user-profile.md 太片面,只反映 AI 对用户认知的冰山一角):

```
1. $VAULT/00-Wiki/user-profile.md          # 基础 + 当前真问题(用户手动 + AI 自动同步)
2. $VAULT/00-Wiki/vault-topics-summary.md  # 15 个 topics + 4 个 concepts 索引,知识地图
3. $VAULT/00-Wiki/recent-activity.md       # 近 14 天 vault 变动 + 注意力热度信号
```

### 三个文件的角色分工

| 文件 | 回答什么 | 谁维护 | 更新频率 |
|---|---|---|---|
| **user-profile.md** | "他是谁,关心什么,跳过什么" | 用户 + Stage 10 自动 | 每周变化 |
| **vault-topics-summary.md** | "他的知识地图长什么样,哪些 topic 深哪些浅" | Stage 11 自动 scan topics+concepts/ | 每天扫描 |
| **recent-activity.md** | "他最近实际在想什么,注意力聚焦在哪" | Stage 11 自动 find -mtime -14 | 每天扫描 |

### 三件套使用规则

**Stage 2 价值打分**:
- Influence 维度的"用户对应需求"权重,看 user-profile **当前真问题**
- **加权热度信号**:命中 recent-activity 🔥🔥🔥 的 topic +1 Influence
- **过滤泛 AI**: 跳过非用户档案任何 topic/concept 的 commodity 内容

**Stage 5 引发思考(💭)字段**:
- **必须 cite 具体 vault 文件路径**,不能只说"你想做 AI 副业"
- 优先级: `concepts/xxx.md` (横切判断) > `topics/xxx.md` (具体主题) > `user-profile.md 当前真问题`
- 格式举例:
  - ✅ "你 5/21 刚更新的 `00-Wiki/topics/claude-code.md` 里 [已有 X 判断],这条新信号 [扩展/补充/反驳] 了 Y,建议 Z"
  - ✅ "你 `00-Wiki/concepts/tool-stack-layering.md` 里把 API/CLI/MCP/Skill 分了层,这条 Mainline intent memory 应该归到 [哪一层] 因为 [...]"
  - ❌ "对你的 AI 副业有启发"(太泛,不显示真在跟踪)

**Stage 4 分级 + Stage 7 HTML**:
- 命中 high 覆盖度 topic → 假设用户已懂基础,直接讨论延伸
- 命中 low 覆盖度 topic → 给"补这个 topic 的 evergreen 价值"

**档案不是 read-only**(v6 起):
- 跑 Stage 1 信号源时如果发现用户新增主题 → 更新 user-profile.md 的 #当前真问题 节
- Stage 11 跑完时:重新扫 vault 生成 vault-topics-summary.md 和 recent-activity.md

---

## Stage 1 · Fetch 数据（并发，约 90 个源）

### 1.1 Zara 中心化 Feed（最优先，本地 JSON，0 网络）

```bash
ZARA_DIR=~/.claude/skills/follow-builders
python3 -c "
import json
x = json.load(open('$ZARA_DIR/feed-x.json'))
p = json.load(open('$ZARA_DIR/feed-podcasts.json'))
b = json.load(open('$ZARA_DIR/feed-blogs.json'))
print(f'X: {len(x[\"x\"])} builder, {sum(len(b_[\"tweets\"]) for b_ in x[\"x\"])} tweets')
"
```

### 1.2 RSS 拉取（并发 curl，参见 reading-feeds.md）

### 1.3 Tier C 官方页面（WebFetch）
### 1.4 中文 KOL（28 人）—— 公众号 / X / 小红书 / Bilibili
### 1.5 Evergreen 白名单 rotation 检查

详见 `$VAULT/00-Wiki/reading-feeds.md`。

### 1.6 引用展开（v6 新增）

**所有 quote tweet / 链接到外部内容的推文**，必须**展开引用源**：
- 用 Claude in Chrome 抓 quote 引用的原推文 / 文章
- 不要只看推文表面，要看它在引用什么

例：Sam Altman 发 "new codex ships today! https://t.co/xxx" → 必须抓 t.co 展开后的 @OpenAIDevs 原推（Appshots 功能详情）才能写出有内容的总结。

---

## Stage 2 · 价值打分（3 维加权）

```
Value = (Primary × 0.3) + (Influence × 0.4) + (Recency × 0.3)
```

| 维度 | 10 分 | 5 分 | 0 分 |
|---|---|---|---|
| **Primary** 一手性 | builder 本人 / 官方 | 媒体报道 | 评论员转述 |
| **Influence** 影响力 | Zara 25 + 中文 KOL 28 + Anthropic 官方 | 业内有声 | 无名营销号 |
| **Recency** 时效 | < 24h | < 7d | > 30d 几乎归零（除非 evergreen） |

**Substantive 二次过滤**（v6 强制）：
- ⛔ 跳过：engagement bait、转推无评论、营销推广、应酬贺词、纯心情发声
- ⛔ **跳过非 AI 主题**（除非和用户档案"当前真问题"有强连接）
- ✅ 保留：原创观点、技术洞察、产品发布、行业分析、实操经验

**被跳过的内容直接丢弃，不要进任何 Tier**（v6 核心规则）。

---

## Stage 3 · 时效硬限制 + Evergreen 例外（v6 强化）

### 时效硬规则

| 发布距今 | 默认处理 |
|---|---|
| < 7 天 | ✅ 通过 |
| 7-30 天 | ✅ 通过（必须明确标注"X 天前"） |
| 30-90 天 | ⚠️ 只能进 Tier 2/3，必须有强 substance |
| > 90 天 | ❌ **完全过滤**（除非在 Evergreen 白名单） |

### 时效标注强制

**每条推荐必须明确标注发布时效**，精确到合适的粒度：
- 24h 内：标"X 小时前"
- < 30 天：标"X 天前"
- < 12 个月：标"X 个月前"
- > 12 个月：标"**X 年前**" + 在该条最前面加 "⏳ **历史内容**：" 警示

举例：
- ✅ 正确：「2025-02-27 发布 · **15 个月前** · ⏳ 历史 evergreen」
- ❌ 错误：「2025-02-27 · 约 3 月前」（明显错误，1 年前的内容不能说 3 月前）

### Evergreen 白名单（绕过时效硬限制）

12 篇核心 evergreen（见 reading-feeds.md），每周 rotate 推 1 篇。即便是 1-2 年前的内容，但仍标注准确日期 + 强调 evergreen 价值。

---

## Stage 3.5 · 🚨 信源多样性硬约束(v8.2 新增 · 防全 GitHub 偏置)

GPT-5.5 xhigh reasoning 有"偏好长 substance"的隐性 bias,**默认会全选 GitHub repo 跳过短推/视频/中文 KOL**。强制纠正:

### Tier 1(必读)信源多样性

**Tier 1 共 4-6 条**,**必须跨至少 3 个媒介**:

| 媒介 | 来源举例 | Tier 1 必占名额 |
|---|---|---|
| 🎬 视频/播客 | YouTube / Latent Space / 中文播客 | **至少 1 条** |
| 📱 X 短推 | Zara feed 头部 25 builder / 中文 KOL X | **至少 1 条** |
| 📰 博客/Newsletter | Simon Willison / Eugene Yan / Karpathy / 中文 newsletter | **至少 1 条** |
| 🐙 GitHub | repo / Show HN / 官方 cookbook | 最多 2 条 |
| 🇨🇳 中文圈 | 公众号 / 小红书 / Bilibili / yihui_indie / 黄赟 等 | **至少 1 条**(如 Tier 1 全英文则降到 Tier 2 必占) |

### Tier 2/3 也要分散
- Tier 2(6 条): GitHub 最多 2 条,X 最多 3 条,其余必须是别的媒介
- Tier 3(5 条): 同 Tier 2

### 失败处理
- 如果某媒介当天**真没有 substantive 内容**(比如 YouTube 一整天没头部账号发新视频),允许该媒介名额降为 evergreen 白名单的一条(参考 reading-feeds.md)
- 不允许"我懒得抓 X 所以跳过" — codex 必须**显式 exec curl Zara feed + WebFetch X 公开 nitter 镜像 / RSSHub** 抓 X,且 log 里要能看到这一步
- 不允许"中文 KOL 没动静" — 必须显式抓 reading-feeds.md 中文 KOL 区域(28 人 / 公众号 / 小红书 / Bilibili)

### Stage 11 自检
跑完 Stage 10 后,**核验 reading-log/{date}.md 里 Tier 1 URL 分布**,如果某媒介为 0,在 chat echo 加 `⚠️ 信源多样性: 缺 X 媒介`。

---

## Stage 4 · 3-Tier 分级（v6 重新定义）

| Tier | Value 阈值 | 用户行动 | 推送形式 |
|---|---|---|---|
| 🔴 **Tier 1（必读）** | ≥ 7.5 | 立即读，回答 quiz | 完整深度：讲什么 / 价值点 / 引发思考（3 点结合用户档案） / Quiz / 链接 |
| 🟡 **Tier 2（值得看）** | 5.5-7.5 | 今天有空看 | 中度：标题 / 100 字总结 / 价值点 / 启发 / 链接 |
| 🟢 **Tier 3（背景信号）** | 4-5.5 | 知道发生了 | 短：标题 / 50 字总结 / 1 句价值 / 链接 |
| ❌ 过滤 | < 4 | — | **不进任何 Tier，不存 vault** |

**v6 核心规则**：
- **所有进入 reading-log 的内容都有价值**（不再有"被过滤掉的非 AI 列表"）
- Tier 区别 = 你应该投入多少时间，不是有没有价值
- 7 天去重（查最近 reading-log 的"已推 URL"）

---

## Stage 5 · 总结写法（v7 统一 schema）

### 🚨 硬约束：Tier 1 / Tier 2 / Tier 3 全部使用同一份 6 字段 schema

**唯一区别 = 字数**，不是字段数量。区别在投入时间多少，不是有没有这些维度。

### 6 字段 schema（每条都必须有）

| 字段 | Tier 1 字数 | Tier 2 字数 | Tier 3 字数 | 说明 |
|---|---|---|---|---|
| ① **元数据行** | 完整 | 完整 | 完整 | 📅 时效 + 👤 作者+身份 + 互动数（Tier1）|
| ② **这条在讲什么** | 200-400 字,拆 3-5 段 | 80-150 字, 拆 2 段 | 40-80 字 | **每段最多 3 句话**, 段间穿插视觉(HTML 里), 不允许密集长段 |
| ③ **💎 价值点** | 100-200 字 | 50-80 字 | 30-50 字 | 这条对 AI 圈/对用户的意义 |
| ④ **💭 引发的思考（结合处境）** | 3 点 × 50-100 字 | 1-2 点 × 50 字 | 1 点 × 30 字 | **必须 cite vault-topics-summary 里的具体 topic/concept 路径**（"你 vault `00-Wiki/topics/xxx.md` 里 X..."/"你 5/21 刚改的 `claude-code.md`..."）|
| ⑤ **📖 带着什么思考去读** | 1 段 actionable | 1 句 actionable | 1 句 actionable | 用户拿到后该带着什么 question 去消费 |
| ⑥ **🎯 Quiz 问题 + 答案** | 1 个，深度题 | 1 个，应用题 | 1 个，认知题 | 用 `<details><summary>` 折叠答案；问"应用到你场景怎么做"不是"它讲什么" |
| ⑦ **🔗 链接** | 必须 | 必须 | 必须 | 含 quote tweet 原推 |

### ⚠️ "这条在讲什么"段写法硬约束(v8.2 新增 · 防长段密文)

**禁止**:把 5 个版本号 / 7 个 feature / 多个技术细节塞进同一段 300+ 字。

**必须**: 拆成 3-5 个独立段落(HTML 里每段一个 `<section class="screen">`),每段:
- **一句话主张** + 0-2 句话支撑
- 不超过 3 句话
- 段与段之间在 HTML 里**必须穿插视觉元素**(流程图/对比卡片/translation-block)

**举例 — 同样信息的不同写法**:

❌ 坏(v8.1 实际产出, 一段 250 字):
> Claude Code 连续几个版本把重点放在"agent runtime"的硬问题上。v2.1.149 里 /usage 开始按类别拆解额度消耗,能看到 skills、subagents、plugins、每个 MCP server 分别吃掉多少成本;/diff detail view 支持键盘滚动;Markdown 输出能渲染 GFM task list。更关键的是安全和权限修复:PowerShell 的 cd..、cd\、X: 这类 built-in 函数曾能绕过工作目录检测...

✅ 好(拆 3 段, 中间穿插视觉):
> **它在干嘛**: Claude Code 最近几版把重点从"UI 小修"转向"agent runtime 工程化"。
> [视觉: 时间轴 visual 显示 v2.1.145 → v2.1.149]
> **新功能 — 成本透明**: /usage 现在按类别拆解额度消耗。skills/subagents/plugins/每个 MCP server 各吃多少 token, 你直接看见。
> [视觉: pie chart 示意各类别占比]
> **新功能 — 沙箱修复**: 之前 PowerShell 的 cd.. 能绕过 workspace 检测,git worktree 的 sandbox write allowlist 覆盖了整个 repo root。现在都补上了。
> [视觉: before/after 对比卡片]

### ✅ Few-shot Example —— Tier 1（完整规格，照这个写）

```markdown
### #1 Zara Zhang 开源 Claude Code Lark/Feishu Bridge

**📅 2026-05-22 昨天** · **👤 Zara Zhang · ex-Anthropic / Latent Space** · **互动: 287 ❤️**

**这条在讲什么**：

Zara 开源了 `claude-code-lark-bridge`，把 Claude Code 接进飞书消息系统。核心能力 5 项：
- 📱 手机端 Claude Code（飞书 App 即可调用）
- 🪜 多 session 管理：一个群聊 = 一个独立 session，互不干扰
- 📥 飞书 context 读取：聊天记录 + 文档 + 会议纪要全部能喂给 Claude Code
- ✍️ 飞书文档写作 + 评论 @ 回复（双向）
- 🎴 交互式卡片 UI（不只是文本，能渲染按钮/表单）

**💎 价值点**：

Claude Code 的 UX 革命。飞书是国内 builder 最完整的工作 context（不像 X 是 broadcast 流，飞书是 thread + 文档 + 会议三位一体）。Claude Code 能读这些 = 比 OpenAI Codex/Appshots 拿到的 screen context 更结构化、更全面。这条把"个人 IDE 里的 Claude Code"扩展成"团队协作的 Claude Code"。

**💭 引发的思考（cite 你的档案）**：

1. **直接复用到 data-bp 项目**：你有完整 Lark skill 生态（lark-base/lark-doc/lark-sheets）。Lark Bridge 反向——业务 stakeholder 直接在飞书群里 @ Claude Code 要数据报告，背后跑 SQL → 返卡片。你 vault 里 `data-bp-producer-ai-main` 业务知识库设计可以从这里抄落地路径。
2. **填补 `agentic-systems-theory` low coverage**：Lark Bridge = brain（Claude Code）/hands（飞书 SDK）解耦的典型实现。你 vault 这个 topic 缺真实案例，这是教科书级素材。
3. **AI 副业可能**：飞书技能栈 + Claude Code = 卖给企业的"AI 同事"。开源 fork 加企业定制（权限/审计/审批），ToB 路径明确。

**📖 带着什么思考去读**：

带着"如果飞书同事在群里 @Bridge 拉上周 DAU，整条链路是怎么实现的"这个问题去读源码，重点看消息路由 + 多 session 隔离 + 卡片渲染三块。

**🎯 Quiz**：

<details>
<summary>飞书同事发"帮我拉一下上周 DAU"，Lark Bridge 跑 SQL 发回飞书卡片。最可能卡住的环节是什么？怎么解？</summary>

**答案**：数据库权限/连接配置（企业内网安全限制）。Claude Code 本身没有 DB credential，且大概率跑在本地不在内网。

**解法**：
- 短期：MCP DB Server 暴露给 Claude Code（用 SSE/stdio），把 credential 留在 server 侧
- 长期：封装 API 层（FastAPI），Claude Code 只调高层接口，权限/审计集中管控

放到 data-bp 项目：你应该早就把 DB 访问封装了，Bridge 接进来直接调 API，不暴露 DB。
</details>

**🔗** https://github.com/zarazhangrui/claude-code-lark-bridge
原推: https://x.com/zarazhangrui/status/2057710284920520906
```

### ✅ Few-shot Example —— Tier 2（紧凑版,字段不缺)

```markdown
### T2-1 · Garry Tan（YC 总裁）: 每个人都应该有一个带 GBrain 的 agent

**📅 2026-05-22 昨天** · **👤 Garry Tan · YC 总裁**

**这条在讲什么**：YC 总裁背书"有持久记忆的个人 agent"方向，他认为下一代 AI 产品的 moat 不在模型，在用户专属的长期 context（GBrain 概念）。

**💎 价值点**：行业头部资本对"个人记忆 agent"方向投资意图明确，验证了 vault 系统这条路。

**💭 引发的思考**：你的 vault + skill 系统就是在构建 GBrain 的人工版本——这个方向是对的，但你目前更新靠手动，下一步是不是让 AI 自动维护？

**📖 带着什么思考去读**：带"我的 vault 自动化更新该怎么做"去读，看他暗示了哪种实现路径。

**🎯 Quiz**：<details><summary>YC 既然看好 GBrain，为什么不直接孵化一家做 GBrain 的公司？</summary>**答案**：他们已经在投了（多家 startup），但 GBrain 的 moat 不是技术是数据，需要长时间积累 = 不适合 YC 短周期。这暗示个人 builder 反而有窗口期：你 vault 已经积累 6 个月数据，是先发优势。</details>

**🔗** https://x.com/garrytan/status/2057636167525498961
```

### ✅ Few-shot Example —— Tier 3（精简版,字段还在不能省）

```markdown
### T3-1 · models.dev: 开源 AI 模型规格 + 定价数据库

**📅 2026-05-22 昨天** · HN 50+ 点

**这条在讲什么**：开源数据库,收录主流 AI 模型 context window/token 速度/$ per M tokens/能力对比。

**💎 价值点**：选型时的客观数据来源,不用问每家官网。

**💭 引发的思考**：你 data-bp 项目里多模型 cost stratification 决策时直接查这个表,省掉手动 benchmark。

**📖 带着什么思考去读**：带"我项目里哪个 task 该用哪个模型省钱"去查一次。

**🎯 Quiz**：<details><summary>cost stratification 在 data-bp 上具体怎么落？</summary>**答案**：高频简单查询用 Haiku($0.25/M),复杂分析用 Sonnet($3/M),用户面 Q&A 用 Haiku 兜底+Sonnet fallback。月度 cost 能从 100% Sonnet 降到 30%。</details>

**🔗** https://github.com/anomalyco/models.dev
```

### ⛔ 反例（v6 今天翻车的样子，**禁止**这样写）

```markdown
### 5. Anthropic: Claude Code auto mode
时效: 2026-03-25 59天前
总结: 两层防御...
价值点: ...
🔗 https://...
```

↑ 缺 ④ 引发思考、⑤ 带着思考去读、⑥ Quiz —— **不合规，必须重写**。

---

---

## Stage 5.5 · ⚡ Self-Check Checklist（v7 新增 · 防字段缺失硬关卡）

> **写完 reading-log/{date}.md 后、推 Discord 前，必须 Read 自己写的文件，对每条记录跑下面 checklist，缺任何一项就回到 Stage 5 补写。全部 ✅ 才进入 Stage 6。**

### 流程

```
1. Read $VAULT/01-Sources/reading-log/{date}.md
2. 对每条 Tier 1/2/3 记录,跑下面 7 项 check
3. 不合规的记录,回 Stage 5 补字段(用 Edit 工具,不要重写整个文件)
4. 重新 Read 验证 → 全 ✅ 才往下
5. echo "✅ Self-check passed: Tier1 N/N, Tier2 M/M, Tier3 K/K, 全 6 字段在场"
```

### Checklist（每条记录逐项验）

| # | 字段 | 通过条件 | 失败动作 |
|---|---|---|---|
| 1 | 元数据行 | 含 📅 时效 + 👤 作者（Tier3 可只有 📅） | 补元数据行 |
| 2 | 「这条在讲什么」段 | 有标题"这条在讲什么"或"总结"，正文 ≥ 字数下限 | 扩写 |
| 3 | 「💎 价值点」段 | 有 💎 emoji + 独立段落 | 补段 |
| 4 | 「💭 引发的思考」段 | 有 💭 emoji + 必须 cite 至少 1 个 user-profile 字段（data-bp / agentic-systems-theory / AI 副业 / vault / Claude Code 等） | 补段 + cite 档案 |
| 5 | 「📖 带着思考去读」段 | 有 📖 emoji + 1 句 actionable | 补段 |
| 6 | 「🎯 Quiz」段 | 有 🎯 emoji + `<details>` 折叠的问题+答案 | 补 Quiz |
| 7 | 「🔗 链接」 | 有 🔗 + 至少 1 个 URL | 补链接 |

### 额外文件级 check

| # | 文件级 check | 通过条件 |
|---|---|---|
| F1 | md frontmatter 后含 HTML 跳转 | 必须有 `[📖 查看 HTML 杂志（含目录）](./{date}.html)` 一行 |
| F2 | HTML 双栏布局 | grep `<aside class="sidebar"` ≥ 1 |
| F3 | HTML sidebar 含 Tier 1/2/3 锚点 | grep `nav-section` ≥ 3 |
| F4 | HTML 文件 ≥ 40KB | 太小说明缩水 |

### 反复执行最多 3 轮

如果第 3 轮还有不合规记录，echo `⚠️ Self-check 第 3 轮仍未全 pass,残缺记录: [...]`，**仍继续推送**（不阻塞），但在 chat echo 标记 ⚠️。

---

## Stage 5.6 · ⚡ 写 extras.json (v9 新增 · 让 render.py 出富视觉)

> **目的**: HTML 渲染由 `render-html.py` 固定模板做,**但 metaphor / features / SVG 流程图这些"内容增强"需要你这个 LLM 来想**。把它们写进同目录的 `{date}.extras.json`,render.py 会读取并出富视觉。

### 路径

```
$VAULT/01-Sources/reading-log/{date}.md          # Stage 5 已写
$VAULT/01-Sources/reading-log/{date}.extras.json # 现在要写
```

### Schema(严格 JSON)

```json
{
  "t1-1": {
    "metaphor": "一句独特比喻 30-80 字 — 必须基于本条具体事实(产品/数字/场景),禁止 default 模板",
    "features": [
      {"emoji": "📊", "title": "短标题 ≤8 字", "desc": "1 句解释 15-30 字"},
      {"emoji": "🔧", "title": "...", "desc": "..."}
    ],
    "flow": ["节点1 ≤8字", "节点2", "节点3", "节点4", "节点5"]
  },
  "t1-2": {...},
  ...
  "t3-5": {...}
}
```

### 三个字段的硬约束

**① metaphor(必填,每条必须独特)**:
- 用一个生活/工程的具体场景类比这条信号
- 必须显式提到本条的关键事实(产品名/数字/场景),否则等于通用模板
- ❌ 禁止: "这条把今天的 AI 工程趋势落到了可执行层" / "想象一下..." 这类空话
- ✅ 范例(Mainline intent memory):
  > "想象你接手一个老项目,前任 git log 里只写 'fix bug'。Mainline 给 agent 加了'同事手册',让它动手前能看到'这块代码以前为什么不删 CSV 接口 — 因为 3 个企业客户夜间对账还在用'。"

**② features(必填,4-6 个)**:
- 拆这条信号的 4-6 个关键 sub-feature
- 每个 feature = emoji(从 📊⚙️🔍💡🚀🛡️🧩📡🎯🔧🌐🪝 选)+ title(≤8 字)+ desc(15-30 字)
- 像产品页那种"这个产品的 6 大功能"那种风格

**③ flow(必填,4-5 个节点)**:
- 这条信号背后的流程/转换/状态机
- 每个节点 ≤8 字(短文字 + 中文优先)
- 渲染成 SVG 数据流图(节点 → 箭头 → 节点)

### Tier 2/3 也要写

不是只 Tier 1 写!**所有 16 条(5 Tier1 + 6 Tier2 + 5 Tier3)都必须有 metaphor + features + flow**。否则 render.py 输出 Tier 2/3 时会缺富视觉,跟 Tier 1 不一致(用户明确要求"格式完全一致")。

### 落盘方式

```bash
cat > $VAULT/01-Sources/reading-log/{date}.extras.json << 'EOF'
{
  "t1-1": {...}, ...
}
EOF
```

### 自检

写完后 `cat $VAULT/01-Sources/reading-log/{date}.extras.json | python3 -m json.tool` 确认 JSON 合法。

---

## Stage 6 · 双语规则（v6 简化）

- **不再要 EN 段 + ZH 段并列**
- 默认全中文
- **关键术语保留英文**：LLM, agent, harness, context, RAG, MCP, RLHF, fine-tune, prompt, token, transformer, embedding, inference, sandbox, multimodal 等
- **专有名词保留英文**：人名、产品名、公司名（如 Karpathy、Anthropic、Claude Code）
- **引用原文金句**：保留英文原文 + 中文翻译（仅用于"金句"段，不是全文双语）

---

## Stage 7 · HTML 渲染 (v9 大改 · 调 render-html.py 不自己写)

> **决定性改动**: 不再让你自己拼 HTML 字符串. HTML 风格由 `~/.claude/scripts/render-html.py` 固化:配色/字体/sidebar/卡片/tooltip/响应式 SVG 全在脚本里. 你只需调用脚本,脚本读 md + extras.json → 输出 HTML.

### 执行

```bash
exec: python3 ~/.claude/scripts/render-html.py \
  $VAULT/01-Sources/reading-log/{date}.md \
  $VAULT/01-Sources/reading-log/{date}.html
```

### 前置条件 (你前面 Stage 5 + 5.6 必须做完)

| 文件 | 谁负责 | 状态 |
|---|---|---|
| `{date}.md` | 你 (Stage 5) | 必须存在,16 条全 7 字段 |
| `{date}.extras.json` | 你 (Stage 5.6) | 必须存在,16 条全有 metaphor/features/flow |
| `{date}.html` | render.py | 自动生成,你不要手写 |

### 自检

```bash
# 验证产物
stat $VAULT/01-Sources/reading-log/{date}.html
# 文件大小应 > 100KB (extras 齐全时)

# 检查关键元素
grep -c 'metaphor-callout' {date}.html  # 应 ≥ 16
grep -c 'features-grid' {date}.html      # 应 ≥ 16
grep -c '<svg' {date}.html               # 应 ≥ 16
```

### 失败处理

- render.py 不存在 → echo 错误,跳过 HTML 生成但继续 Stage 8 (Discord 仍推)
- extras.json 不存在 → render.py 仍能跑(降级,只缺富视觉),不算失败
- 产物 < 50KB → 警告但不阻塞,在 chat echo 加 ⚠️

### 为什么这样设计

之前(v8 / v8.2): 你每天自己写 HTML,风格每天都飘 — 5/23 杂志风,5/24 双栏,5/25 教程风,用户无法形成稳定阅读习惯.
现在(v9): 模板固定在代码里,你只负责写 metaphor/features/flow 的"内容素材",HTML 拼装由脚本做.
- 风格 100% 稳定
- 改样式 = 改 render.py (一次永久)
- 改内容方向 = 改 prompt (一次永久)

### 输出位置 (不变)
`$VAULT/01-Sources/reading-log/{YYYY-MM-DD}.html`

---

## Stage 8 · Discord 推送(v8 大改 · "预告片"模式)

**核心定位变了**: Discord 不再塞完整内容,**Discord 是预告片,HTML 是正片**。
原因: Discord 每块硬限制 1900 字符,塞不下 6 字段深度内容,堆字让人没欲望点。

### 新策略

每条 Tier 1/2/3 在 Discord 用 **emoji 钩子 + 一句卖点 + HTML 锚点链接**, 引导用户去看 HTML 详细版。

### Block 设计(v8)

```bash
source ~/.follow-builders/.env
WEBHOOK="${DISCORD_WEBHOOK_URL}?wait=true"   # ← 必须 ?wait=true 保证顺序
```

#### Block 1 — 头部预告(开胃菜)

```
📰 **AI Digest 2026-05-24**

今日 Tier 1: 4 条 · Tier 2: 6 条 · Tier 3: 5 条

🎯 **三条钩子(挑你最想看的一条)**:
1️⃣ Zara 开源飞书 + Claude Code 桥 — 你 lark-skill 生态可以直接复用
2️⃣ Yann Dubois 判断 harness 不消亡但会变轻 — 直接打脸 vault `agentic-systems-theory`
3️⃣ Anthropic Macro Evals — 你 data-bp 项目落地拆 trace/eval/sandbox 三件套的可参考实现

📖 **完整深度阅读(强烈推荐)**: file://~/Documents/obsidian/bgggcontent/01-Sources/reading-log/2026-05-24.html
```

#### Block 2-N — 每条 Tier 1 一块预告片(v8.2 严格模板)

**每块必须包含 5 段, 一段都不能少, 也不能用 default 文案**:

1. 📅 时效 · 👤 作者 + 互动数
2. **💎 价值点(1-2 句)**: 这条**为什么重要**(不是泛泛"AI 工程趋势",要具体到本条揭示的模式)
3. **💭 命中你的 vault(1-2 句)**: cite `00-Wiki/topics/xxx.md` 或 `00-Wiki/concepts/xxx.md` 具体路径,说**这条扩展/补充/反驳了你已有的什么判断**(不是 "建议放进知识链" 这种 default)
4. **📖 去 HTML 看什么(1 句)**: 提示用户**HTML 正片里多了什么**(metaphor / 流程图 / Quiz / vault 跳转链接)
5. **🔗 原文链接 + 📖 HTML#锚点 跳转**

例:
```
🟥 **Tier 1 #1 · Zara Zhang 开源飞书 Claude Code Bridge**
📅 昨天 · 👤 Zara(ex-Anthropic) · ❤️ 287

💎 **价值点**: Claude Code 从"个人 IDE"扩展到"团队协作 agent" — 飞书 thread + 文档 + 会议三位一体的工作 context, 比 OpenAI Codex 拿到的 screen context 完整得多.

💭 **命中 vault**: 你 `00-Wiki/topics/claude-code.md` (high 覆盖)写了 Claude Code 是反复循环代理过程, 这次把"循环边界"从本地扩展到飞书生态; 同时你 `00-Wiki/concepts/tool-stack-layering.md` 的 Skill 层有了新案例.

📖 HTML 详解: 含飞书消息路由 + 多 session 隔离的流程图, 还有 "data-bp 同事 @ 拉 SQL" 的 Quiz.

🔗 https://github.com/zarazhangrui/claude-code-lark-bridge
📖 file://...reading-log/2026-05-24.html#t1-1
```

每块字符数约 **500-700**, 紧凑但每条都独立(禁止 default 重复文案)。

### 🚨 v8.2 严禁 default 文案

以下 default 句式**绝对禁止出现**(v8.1 翻车了):
- ❌ "这条把今天的 AI 工程趋势落到了可执行层"
- ❌ "建议放进今天的 agent 工程知识链"
- ❌ "这条值得关注"
- ❌ "对你的 vault 有补充"(不带具体路径)

如果你写不出来具体的 💎 价值点 / 💭 vault cite, 说明你对这条内容理解不够 → 回 Stage 5 重新写,不要用 default 凑数。

#### Block N+1 — Tier 2 集合(更紧凑)

每条只 1 行: `🟡 标题 · 一句钩子 · 🔗 链接 · HTML#t2-x`

#### Block N+2 — Tier 3 集合

每条只半行,纯标题 + 链接 + HTML 锚点。Tier 3 在 Discord 是"知道发生了就够",深度去 HTML 看。

### 视觉风格

- 用 emoji 区分 Tier:🟥 Tier 1 / 🟡 Tier 2 / 🟢 Tier 3
- 用 Discord 的 markdown 加粗(`**`)/斜体(`*`)/代码块(`` ` ``)/quote(`> `)
- **绝对不允许**在 Discord 塞整段"讲什么"长文字 — 那个内容只在 HTML 出现

### 顺序保证

`?wait=true` 让每条 POST 同步等 Discord ACK 后再发下一条 → 完全保证顺序。失败 retry 1 次。

---

## Stage 9 · vault 存档（v7 强制 HTML 跳转）

写入 `$VAULT/01-Sources/reading-log/{YYYY-MM-DD}.md`

### 🚨 v7 强制：md frontmatter 后必须有 HTML 跳转链接

frontmatter 紧接的第二段（在大标题 `# AI Digest {date}` 之后），必须有一行可点击跳转：

```markdown
---
type: reading-log
date: 2026-05-23
...
---

# AI Digest 2026-05-23

> 📖 **[查看 HTML 杂志（含目录）](./2026-05-23.html)** — 含 sidebar TOC、Quiz 折叠、SVG 可视化

---

## 🔴 Tier 1 ...
```

**注意是 markdown 普通链接 `[text](./xxx.html)`，不是 Obsidian wikilink `[[xxx.html]]`** —— wikilink 在 Obsidian 里点不开 HTML 文件，必须用普通链接。

### 内容

同 Discord 推送但更完整（含 PROFILE 审计部分 + Stage 5 的完整 6 字段）。

---

## Stage 10 · 完成确认 + 用户档案更新

### v7 推荐执行顺序

```
Stage 1-4: 抓 + 打分 + 分级
Stage 5:   写 reading-log/{date}.md (Tier 1/2/3 全 6 字段)
Stage 5.5: Self-check (最多 3 轮) → 全 pass / 标 ⚠️
Stage 7:   写 reading-log/{date}.html (强制 sidebar + TOC)
Stage 9:   md 顶部插 HTML 跳转链接（如未在 Stage 5 写入）
Stage 8:   Discord 推送（顺序保证）  ← 注意：放最后，确保 md/html 已就绪
Stage 10:  echo + 更新 user-profile.md
```

### chat echo 行（v7 升级）

```
✅ Daily Digest v7 已推 Discord (T1: N, T2: M, T3: K) + HTML 含 sidebar + md 含跳转 + self-check: <pass|⚠️ 残缺X条>
```

例：
- 全 pass: `✅ Daily Digest v7 已推 Discord (T1: 4, T2: 6, T3: 5) + HTML 含 sidebar + md 含跳转 + self-check: pass`
- 部分残缺: `✅ Daily Digest v7 已推 Discord (T1: 4, T2: 6, T3: 5) + HTML 含 sidebar + md 含跳转 + ⚠️ self-check: T2-3 缺 Quiz / T3-2 缺引发思考`

### 用户档案更新

**如果今日 PROFILE 信号显示用户新增重点**(如新项目、新主题), **主动更新 user-profile.md 的 #当前真问题 节**

---

## Stage 11 · 自动维护 vault 三件套(v8 新增)

完成 Discord 推送后,**必须**重新生成两个索引文件,让明天的 daily-digest 拿到最新 vault 状态。

### 11.1 重新生成 vault-topics-summary.md

```bash
# 扫描 00-Wiki/topics/*.md 和 00-Wiki/concepts/*.md
# 提取每个 file 的 H1 + 第一段非空内容 + coverage_overall + source_count + last_compiled
# 按覆盖度分组(high/medium/low)排好
# 写回 $VAULT/00-Wiki/vault-topics-summary.md
```

如果有**新增 topic/concept 文件**(用户在 vault 里手动加的) → 自动收录进索引,加上"⭐ 新增"标记。
如果有**删除文件** → 从索引移除。

### 11.2 重新生成 recent-activity.md

```bash
# find $VAULT -name "*.md" -mtime -14 -not -path "*/.*" | sort by mtime desc
# 按时间倒序列出近 14 天所有 .md 文件变动
# 计算 7 天热度信号: 同一 topic 被改了几次
# 区分: 🔥 当前注意力 / 📊 7 天热度 / ⚪ 静默主题
# 写回 $VAULT/00-Wiki/recent-activity.md
```

### 11.3 自检三件套写入是否成功

```bash
stat $VAULT/00-Wiki/{user-profile,vault-topics-summary,recent-activity}.md
# 确认三个文件的 mtime 都是今天
```

### 失败处理

- 11.1 / 11.2 失败 → 不阻塞,但在最后 echo 加 `⚠️ Stage 11 vault sync 失败` 标记
- 11.3 自检失败 → 同上,标记但不 fail-fast(因为 Discord 已经推送了)

---

## 重要约束

| 约束 | 说明 |
|---|---|
| **必读 user-profile** | Stage 0 强制 |
| **focus AI** | 跳过非 AI 主题 |
| **价值导师** | AI own 价值判断 |
| **中文为主** | 关键术语英文 |
| **时效精确标注** | 不能 1 年前说 3 月前 |
| **无价值不进 Tier** | Tier 3 也要有价值 |
| **3+ 媒介强制** | X / 视频 / 播客 / 博客 / GitHub |
| **HTML 可视化** | 不能纯文字（参考 codebase-to-course） |
| **顺序推送** | `?wait=true` 保证 |
| **审计透明** | reading-log 完整审计每条评分 |
| **降级不崩** | 任何源失败跳过 |
| **更新档案** | 主动更新 user-profile.md |

---

## 工具备忘

- 用户档案：`$VAULT/00-Wiki/user-profile.md` ⭐ **每次必读**
- Zara feed：`~/.claude/skills/follow-builders/feed-*.json`
- feed-prompts：`$VAULT/00-Wiki/feed-prompts/`
- reading-feeds：`$VAULT/00-Wiki/reading-feeds.md`
- Discord webhook：`~/.follow-builders/.env` 的 `DISCORD_WEBHOOK_URL`
- vault：`$VAULT`
- 工具：curl, gh, python3, jq, WebFetch, Bash, mcp__Claude_in_Chrome__*

#!/usr/bin/env python3
"""
render-html.py — daily-digest HTML 渲染器 (v9 风格固化)

用法:
    python3 render-html.py <reading-log-md-path> [<output-html-path>]
    # 不指定 output → 同目录同名 .html

设计:
    - 输入: reading-log/{date}.md (frontmatter + 三级标题 ### #N 文章)
    - 输出: reading-log/{date}.html (双栏 sidebar + 杂志卡片风)
    - 风格混合: 5/25 当前的目录/模块结构 + 5/23 的字体/配色/卡片视觉
    - 设计哲学: HTML 风格固化, 不让 LLM 临场发挥 → 每天产物风格稳定

实现:
    - 双栏 layout, 左侧 sticky sidebar TOC
    - Tier 1: 白色卡片 + 浅绿 hero 渐变, 含 metaphor callout + 自动 emoji 特征 grid + 内嵌 SVG
    - Tier 2: 双列 grid 卡片
    - Tier 3: 紧凑表格
    - 40+ 词术语 tooltip (CSS+JS popup)
    - vault link (obsidian://) 自动检测
    - <details> Quiz 折叠
"""
import re
import sys
import html
from pathlib import Path
from datetime import datetime

# ============ 术语 tooltip 白名单 (40+ 词) ============
TERMS = {
    "LLM": "大语言模型,通过预训练 + 微调学到语言能力的神经网络",
    "agent": "能观察环境/调用工具/循环完成目标的 AI 程序,不只是一次聊天回复",
    "Agent": "能观察环境/调用工具/循环完成目标的 AI 程序,不只是一次聊天回复",
    "agentic": "agent 风格的,指通过工具调用 + 循环逻辑完成复杂任务",
    "harness": "包住模型的工程外壳,负责工具/权限/状态/重试/验证",
    "MCP": "Model Context Protocol,统一协议让模型连外部工具/数据源",
    "RAG": "Retrieval-Augmented Generation,先检索再生成,补足模型知识缺口",
    "sandbox": "隔离执行环境,用边界限制代码/文件/网络副作用",
    "RLHF": "人类反馈强化学习,用人评分把模型对齐到 helpful/harmless",
    "RLVR": "Reinforcement Learning with Verifiable Rewards,用可自动验证的奖励训练",
    "fine-tune": "微调,在预训练基础上用领域数据继续训练",
    "token": "模型处理的最小语言单位,~1 个汉字或 0.75 个英文单词",
    "context": "上下文窗口,模型一次能看到的 token 数量",
    "inference": "推理,把输入跑过模型得到输出",
    "transformer": "LLM 的核心架构,基于 self-attention 机制",
    "embedding": "向量化,把文本转成数字向量便于检索/聚类",
    "multimodal": "多模态,模型能同时处理文字/图片/音频/视频",
    "agent loop": "agent 的核心循环: 观察 → 思考 → 行动 → 反思 → 再观察",
    "chain-of-thought": "思维链,让模型输出中间推理步骤而非直接结论",
    "reasoning effort": "推理预算等级,low/medium/high/xhigh 控制模型 thinking tokens",
    "prompt engineering": "设计提示词的工程方法",
    "prompt injection": "攻击者通过用户输入篡改模型指令的安全漏洞",
    "trace": "agent 一次完整执行的事件日志,用于复盘和调试",
    "eval": "评估,用 benchmark 测模型/agent 在特定任务的表现",
    "macro eval": "系统级评估,看多个 trace 汇总后的 pattern 而非单条",
    "observability": "可观测性,系统状态可被外部监控/审计/复盘",
    "webhook": "HTTP 回调,事件发生时主动 POST 通知外部",
    "OAuth": "第三方授权协议,允许 app 代替用户访问其他服务",
    "API": "应用程序接口,程序之间的通信约定",
    "CLI": "命令行接口,通过 terminal 输入命令调用程序",
    "SDK": "软件开发工具包,包装 API 给开发者用",
    "skill": "Anthropic Skill 系统,把工作流封装成可复用的 Claude 技能",
    "Skill": "Anthropic Skill 系统,把工作流封装成可复用的 Claude 技能",
    "plugin": "插件,把第三方功能集成进主程序的扩展机制",
    "launchd": "macOS 的系统级定时任务管理器,替代传统 cron",
    "cron": "Unix 定时任务调度器,按时间触发命令",
    "daemon": "守护进程,后台长期运行的程序",
    "websocket": "全双工 TCP 连接,服务器可主动推消息给浏览器",
    "SSE": "Server-Sent Events,服务器单向流式推送数据",
    "REPL": "Read-Eval-Print-Loop,交互式语言环境",
    "frontmatter": "文件头部的元数据块,通常用 YAML 写",
    "repository": "git 代码仓库",
    "pull request": "把代码改动提交到主分支前的审查请求",
    "backfill": "用历史数据填补新加字段或追溯计算",
    "idempotent": "幂等,同一操作执行多次效果跟一次相同",
    "ORM": "对象关系映射,用程序对象操作数据库,自动生成 SQL",
    "SIEM": "安全信息和事件管理系统,集中收集 + 分析安全日志",
    "DLP": "数据防泄漏,识别 + 阻止敏感信息外流",
    "SASE": "安全访问服务边缘,统一云端网络安全架构",
    "DAU": "Daily Active Users,日活跃用户数",
    "GMV": "Gross Merchandise Value,商品交易总额",
    "endpoint": "API 接口的具体 URL 入口",
    "schema": "数据结构定义,约定字段名/类型/约束",
    "patch": "代码补丁/小修改",
    "diff": "文件差异对比",
}

# emoji pool 用于自动生成特征 grid (从 markdown 加粗短语提取)
GRID_EMOJIS = ["📦", "⚙️", "🔍", "💡", "🚀", "🛡️", "🧩", "📊", "🎯", "🔧", "🌐", "📡"]

# ============ Parser ============

def parse_frontmatter(text):
    """解析 YAML frontmatter, 返回 dict + 剩余 body"""
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.DOTALL)
    if not m:
        return {}, text
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    cur_key = None
    for line in fm_text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        if line.startswith('  - '):  # list item
            if cur_key and isinstance(fm.get(cur_key), list):
                fm[cur_key].append(line[4:].strip())
            continue
        if re.match(r'^[a-zA-Z_]+:\s*$', line):  # block scalar
            cur_key = line.split(':')[0].strip()
            fm[cur_key] = []
            continue
        if ':' in line:
            k, _, v = line.partition(':')
            cur_key = k.strip()
            v = v.strip()
            if not v:
                fm[cur_key] = []
            else:
                fm[cur_key] = v
    return fm, body


def parse_articles(body):
    """解析 ### 三级标题文章列表"""
    # 按 ### 切块
    parts = re.split(r'(?m)^### ', body)
    articles = []
    for i, p in enumerate(parts):
        if not p.strip():
            continue
        # 第一行是标题
        lines = p.split('\n')
        title_line = lines[0].strip()
        rest = '\n'.join(lines[1:])

        # 跳过非文章 H3 (比如 PROFILE 审计后面的)
        if not re.match(r'^(#\d+|T[123]-\d+)', title_line):
            continue

        # 解析 tier + id
        m = re.match(r'^(#(\d+)|T(\d)-(\d+))\s*·?\s*(.+)$', title_line)
        if not m:
            continue
        if m.group(2):  # #N → Tier 1
            tier = 1
            n = int(m.group(2))
            anchor = f"t1-{n}"
        else:
            tier = int(m.group(3))
            n = int(m.group(4))
            anchor = f"t{tier}-{n}"
        title = m.group(5).strip()

        art = {
            'tier': tier, 'n': n, 'id': anchor, 'title': title,
            'meta': '', 'whats': '', 'value': '', 'thoughts': [],
            'reading_prompt': '', 'quiz_q': '', 'quiz_a': '', 'links': []
        }

        # parse 字段块
        # meta 行: 第一段 **📅 ... · 👤 ...**
        section_text = rest
        meta_m = re.search(r'\*\*(📅[^*]+)\*\*', section_text)
        if meta_m:
            art['meta'] = meta_m.group(1).strip()

        # 各字段段: **这条在讲什么**: ... **💎 价值点**: ... 等
        # 用分割法
        sections = re.split(r'\*\*(这条在讲什么|💎 价值点|💭 引发的思考[^*]*|📖 带着什么思考去读|🎯 Quiz|🔗 链接)\*\*[:：]?\s*\n*',
                            section_text)
        # sections = [前缀, key1, body1, key2, body2, ...]
        for j in range(1, len(sections) - 1, 2):
            key = sections[j].strip()
            val = sections[j + 1].strip()
            # 砍掉后面的 ---
            val = re.split(r'\n---', val)[0].strip()
            if '讲什么' in key:
                art['whats'] = val
            elif '价值点' in key:
                art['value'] = val
            elif '引发' in key:
                # 解析 1. xxx 2. xxx 3. xxx
                thought_items = re.findall(r'(?m)^\d+\.\s*(.+?)(?=\n\d+\.|\n\n|\Z)', val, re.DOTALL)
                art['thoughts'] = [t.strip() for t in thought_items] if thought_items else [val]
            elif '带着' in key:
                art['reading_prompt'] = val
            elif 'Quiz' in key:
                # 解析 <details><summary>Q</summary>A</details>
                qm = re.search(r'<details>\s*<summary>(.*?)</summary>(.*?)</details>', val, re.DOTALL)
                if qm:
                    art['quiz_q'] = qm.group(1).strip()
                    art['quiz_a'] = qm.group(2).strip()
                else:
                    art['quiz_q'] = val
            elif '链接' in key:
                urls = re.findall(r'https?://[^\s)>]+', val)
                art['links'] = urls

        # 自动提取 emoji 特征 grid 候选 (从"讲什么"段找加粗短语)
        bold_phrases = re.findall(r'\*\*([^\d][^*]{2,30})\*\*', art['whats'])
        # 过滤掉太长/含标点的
        candidates = []
        for p in bold_phrases:
            p = p.strip().rstrip(':：,，.。;；!！?？')
            if 2 <= len(p) <= 25 and not re.search(r'[\.。:：;；]', p):
                candidates.append(p)
        art['features'] = candidates[:6]  # 最多 6 个

        articles.append(art)
    return articles


# ============ Renderer ============

def wrap_terms(text):
    """把术语包装成 .term tooltip span (HTML 转义后)"""
    # 先 escape, 再注入 (这样 user-facing 安全)
    text = html.escape(text)
    # 按词长降序匹配, 避免 short term 抢先
    for term in sorted(TERMS.keys(), key=len, reverse=True):
        # 用 \b 边界, 仅匹配独立单词
        pattern = re.compile(r'\b' + re.escape(term) + r'\b')
        def repl(m, t=term):
            return f'<span class="term" data-def="{html.escape(TERMS[t])}">{m.group(0)}</span>'
        text = pattern.sub(repl, text, count=1)  # 每个术语全文只 tooltip 第一次出现
    return text


def render_paragraphs(text):
    """把 markdown 段落转 HTML <p>, 处理 **bold** + 行内 code"""
    text = text.strip()
    # 行内格式
    def md_to_html(s):
        s = wrap_terms(s)
        # **bold** -> <strong>
        s = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', s)
        # `code` -> <code>
        s = re.sub(r'`([^`]+?)`', r'<code>\1</code>', s)
        return s

    parts = re.split(r'\n\n+', text)
    return '\n'.join(f'<p>{md_to_html(p.strip())}</p>' for p in parts if p.strip())


def detect_vault_links(text):
    """从文本里抓 00-Wiki/topics/xxx.md 之类的 vault 路径, 加 obsidian:// 跳转"""
    pattern = re.compile(r'`(00-Wiki/[\w/\-]+\.md)`')
    def make_link(m):
        path = m.group(1)
        # obsidian url: 把斜杠转, 去掉 .md
        file_part = path.replace('.md', '').replace('/', '%2F')
        return f'<a href="obsidian://open?vault=bgggcontent&file={file_part}" class="vault-link" title="打开 vault 文件">📂 <code>{path}</code></a>'
    return pattern.sub(make_link, text)


def render_features_grid(features):
    """生成 2×3 emoji 特征 grid

    features 可以是:
      - list of str: 简单文字, 自动配 emoji
      - list of dict: {"emoji": "📊", "title": "X", "desc": "Y"} 完整结构 (来自 extras.json)
    """
    if not features or len(features) < 2:
        return ''
    items_html = []
    for i, feat in enumerate(features):
        if isinstance(feat, dict):
            # 高质量结构 (LLM 写入 extras.json)
            emoji = feat.get('emoji', GRID_EMOJIS[i % len(GRID_EMOJIS)])
            title = feat.get('title', '')
            desc = feat.get('desc', '')
            items_html.append(
                f'<div class="feat"><span class="feat-emoji">{emoji}</span>'
                f'<div class="feat-body"><div class="feat-title">{wrap_terms(title)}</div>'
                f'<div class="feat-desc">{wrap_terms(desc)}</div></div></div>'
            )
        else:
            # 降级: 仅文字
            emoji = GRID_EMOJIS[i % len(GRID_EMOJIS)]
            items_html.append(
                f'<div class="feat"><span class="feat-emoji">{emoji}</span>'
                f'<span class="feat-text">{wrap_terms(str(feat))}</span></div>'
            )
    return f'<div class="features-grid">{"".join(items_html)}</div>'


def render_flow_svg(article):
    """根据文章 flow 字段生成 SVG 数据流图. 优先用 extras.json 的 flow, 降级用 features"""
    # 优先用 extras 里的 flow (LLM 写, 是真正的流程节点)
    flow = article.get('flow') or []
    if flow and len(flow) >= 2:
        nodes = [n if isinstance(n, str) else n.get('label', '') for n in flow][:5]
    else:
        # 降级: 从 features 字符串/dict 提取
        feats = article.get('features') or []
        if not feats or len(feats) < 3:
            return ''
        nodes = []
        for f in feats[:4]:
            if isinstance(f, dict):
                nodes.append(f.get('title', ''))
            else:
                nodes.append(str(f))
    n = len(nodes)
    if n < 2:
        return ''
    # 动态 box 宽度根据节点最长字数 (中文 ~14px, 英文 ~7px)
    max_chars = max(len(s) for s in nodes)
    box_w = max(110, min(160, max_chars * 16 + 20))
    arrow_gap = 24
    width = box_w * n + arrow_gap * (n - 1)
    # ↑ width 用于 viewBox(原始坐标),CSS 用 max-width 自动缩到容器宽
    colors = [('#e3f2fd', '#1976d2'), ('#fff3e0', '#cc785c'),
              ('#e8f0e0', '#2d5016'), ('#f5e6e7', '#c4747a'),
              ('#fef3c7', '#d97706')]
    rects = []
    for i, label in enumerate(nodes):
        x = i * (box_w + arrow_gap)
        bg, stroke = colors[i % len(colors)]
        # 中文节点不截短, 用 box_w 适配
        rects.append(
            f'<rect x="{x:.0f}" y="20" width="{box_w}" height="46" rx="8" '
            f'fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>'
            f'<text x="{x + box_w/2:.0f}" y="48" text-anchor="middle" font-size="13" fill="{stroke}" font-weight="500">{html.escape(label)}</text>'
        )
        if i < n - 1:
            x1 = x + box_w
            x2 = x + box_w + arrow_gap
            rects.append(
                f'<line x1="{x1:.0f}" y1="43" x2="{x2:.0f}" y2="43" '
                f'stroke="#4a7c2f" stroke-width="2" marker-end="url(#ar1)"/>'
            )
    # 用 viewBox + preserveAspectRatio 让 SVG 自动响应式缩到容器宽度
    svg = (
        f'<div class="svg-wrap">'
        f'<svg viewBox="0 0 {width} 86" preserveAspectRatio="xMidYMid meet" '
        f'xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;max-height:90px">'
        '<defs><marker id="ar1" markerWidth="7" markerHeight="7" refX="5" refY="2.5" orient="auto">'
        '<path d="M0,0 L0,5 L7,2.5 z" fill="#4a7c2f"/></marker></defs>'
        + ''.join(rects) +
        '</svg>'
        '<div class="svg-caption">↑ 流程图 · 滚动/缩放看完整</div>'
        '</div>'
    )
    return svg


def make_metaphor(article):
    """生成 metaphor callout. 优先用 extras.json 的 (LLM 写,独特), 没有就返回空(不显示降级 fallback)"""
    meta = article.get('metaphor_extra')
    if meta:
        return wrap_terms(meta)
    return None  # 不显示 default fallback, 避免污染


TIER_META = {
    1: {'badge': 'b1', 'label': '🔴 Tier 1', 'name': '必读'},
    2: {'badge': 'b2', 'label': '🟡 Tier 2', 'name': '值得看'},
    3: {'badge': 'b3', 'label': '🟢 Tier 3', 'name': '背景信号'},
}


def render_unified_card(art):
    """Tier 1/2/3 统一卡片 (5/23 风,浅绿 hero + 白色 body + 富视觉)
    所有 tier 用同样字段,只换 hero 顶部 badge 颜色和 eyebrow 文案
    """
    tm = TIER_META[art['tier']]
    metaphor_text = make_metaphor(art)
    metaphor_html = f'<div class="metaphor-callout">💡 {metaphor_text}</div>' if metaphor_text else ''
    features_html = render_features_grid(art['features'])
    svg_html = render_flow_svg(art)
    whats_html = render_paragraphs(art['whats'])
    value_html = render_paragraphs(art['value'])

    # thoughts: 3 个 .thought callout, 每个含 vault link
    thoughts_html = ''
    for i, t in enumerate(art['thoughts'], 1):
        body = detect_vault_links(t)
        body = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', body)
        body = re.sub(r'`([^`]+?)`', r'<code>\1</code>', body)
        body = wrap_terms(body) if '<' not in body[:30] else body
        thoughts_html += f'<div class="thought"><span class="thought-num">{i}</span>{body}</div>'

    reading_html = render_paragraphs(art['reading_prompt'])

    quiz_html = ''
    if art['quiz_q']:
        q = wrap_terms(art['quiz_q'])
        a = render_paragraphs(art['quiz_a']) if art['quiz_a'] else ''
        quiz_html = f'<details class="quiz"><summary>🎯 测一下: {q}</summary><div class="answer">{a}</div></details>'

    links_html = ''
    if art['links']:
        links_html = '<div class="link-row">' + ''.join(
            f'<a href="{html.escape(u)}" class="link-btn" target="_blank">原文 {i+1} →</a>'
            for i, u in enumerate(art['links'][:3])
        ) + '</div>'

    return f'''
<article class="card t-card t{art['tier']}-card" id="{art['id']}">
  <div class="hero t{art['tier']}-hero">
    <div class="eyebrow"><span class="badge {tm['badge']}">{tm['label']}</span> &nbsp;·&nbsp; # {art['n']} · {tm['name']}</div>
    <h2 class="card-title">{wrap_terms(art['title'])}</h2>
    <div class="meta-row">{wrap_terms(art['meta'])}</div>
  </div>
  <div class="body">
    {metaphor_html}

    <div class="h3">🔍 这条在讲什么</div>
    {whats_html}

    {features_html}
    {svg_html}

    <div class="h3">💎 价值点</div>
    {value_html}

    <div class="h3">🧠 引发的思考(结合你的 vault)</div>
    {thoughts_html}

    <div class="h3">📖 带着什么思考去读</div>
    {reading_html}

    {quiz_html}
  </div>
  {links_html}
</article>
'''


def render_sidebar(articles, date_str, tier_counts):
    """左侧 sticky sidebar TOC"""
    by_tier = {1: [], 2: [], 3: []}
    for a in articles:
        by_tier[a['tier']].append(a)

    sections_html = []
    for tier, label, color in [(1, '🔴 Tier 1 必读', 'b1'), (2, '🟡 Tier 2 值得看', 'b2'), (3, '🟢 Tier 3 背景信号', 'b3')]:
        items = by_tier[tier]
        if not items:
            continue
        links = '\n'.join(
            f'<a href="#{a["id"]}" data-id="{a["id"]}">#{a["n"]} {html.escape(a["title"][:30])}...</a>'
            for a in items
        )
        sections_html.append(f'<div class="nav-section"><div class="nav-label">{label}</div>{links}</div>')

    return f'''
<aside class="sidebar">
  <div class="sidebar-inner">
    <h1>AI Digest</h1>
    <div class="date">{date_str}</div>
    <div class="micro">HTML 正片 · sidebar · metaphor · tooltip · Quiz</div>
    <nav>{"".join(sections_html)}</nav>
    <div class="sidebar-foot">每天 8:00 自动生成 · v9 渲染器</div>
  </div>
</aside>
'''


def render_html(frontmatter, articles):
    date_str = frontmatter.get('date', datetime.now().strftime('%Y-%m-%d'))
    tier_counts = {1: len([a for a in articles if a['tier'] == 1]),
                   2: len([a for a in articles if a['tier'] == 2]),
                   3: len([a for a in articles if a['tier'] == 3])}

    sidebar = render_sidebar(articles, date_str, tier_counts)

    # v9.1: 所有 tier 用统一卡片模板
    t1_html = '\n'.join(render_unified_card(a) for a in articles if a['tier'] == 1)
    t2_html = '\n'.join(render_unified_card(a) for a in articles if a['tier'] == 2)
    t3_html = '\n'.join(render_unified_card(a) for a in articles if a['tier'] == 3)
    t2_grid = t2_html  # 不再 grid 双列, 用单列统一卡片
    t3_table = t3_html

    css = '''
:root {
  --green: #2d5016;
  --green-pale: #e8f0e0;
  --green-mid: #4a7c2f;
  --cream: #faf7f2;
  --pink: #c4747a;
  --pink-light: #f5e6e7;
  --text: #2c2416;
  --text-muted: #6b5e4a;
  --border: #d4c9b4;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  font-family: -apple-system, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif;
  background: var(--cream);
  color: var(--text);
  line-height: 1.7;
  font-size: 15px;
}
.progress { position: fixed; top: 0; left: 0; height: 3px; background: var(--green); z-index: 100; width: 0; transition: width 0.1s; }

.layout { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }

/* Sidebar */
.sidebar { background: var(--green); color: white; position: sticky; top: 0; height: 100vh; overflow-y: auto; }
.sidebar-inner { padding: 24px 20px; }
.sidebar h1 { font-size: 18px; font-weight: 700; letter-spacing: 0.5px; }
.sidebar .date { font-size: 12px; opacity: 0.7; margin: 4px 0 12px; letter-spacing: 1px; }
.sidebar .micro { font-size: 11px; opacity: 0.6; margin-bottom: 24px; line-height: 1.6; }
.nav-section { margin-bottom: 20px; }
.nav-label { font-size: 11px; text-transform: uppercase; font-weight: 600; opacity: 0.85; margin-bottom: 6px; letter-spacing: 0.5px; }
.sidebar a { display: block; color: rgba(255,255,255,0.78); text-decoration: none; padding: 5px 8px; border-radius: 5px; font-size: 12px; line-height: 1.5; margin-bottom: 2px; }
.sidebar a:hover { background: rgba(255,255,255,0.1); color: white; }
.sidebar a.active { background: rgba(255,255,255,0.15); color: white; font-weight: 600; }
.sidebar-foot { font-size: 10px; opacity: 0.5; margin-top: 30px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.15); }

/* Main */
.main { padding: 30px 40px; max-width: 900px; margin: 0 auto; }

/* Page hero */
.page-hero { background: linear-gradient(135deg, var(--green-pale), white); border: 1px solid var(--border); border-radius: 14px; padding: 30px; margin-bottom: 30px; }
.page-hero .eyebrow { font-size: 11px; color: var(--green); letter-spacing: 2px; text-transform: uppercase; opacity: 0.8; }
.page-hero h1 { font-size: 28px; font-weight: 700; margin: 8px 0 4px; color: var(--green); }
.page-hero .subtitle { font-size: 14px; color: var(--text-muted); margin-bottom: 16px; }
.stats { display: flex; gap: 24px; margin-top: 16px; }
.stat-box { background: white; border: 1px solid var(--border); border-radius: 10px; padding: 12px 18px; min-width: 80px; }
.stat-num { font-size: 24px; font-weight: 700; color: var(--green); display: block; }
.stat-label { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* Section header */
.section-header { display: flex; align-items: center; gap: 10px; margin: 36px 0 20px; padding-bottom: 12px; border-bottom: 2px solid var(--border); }
.badge { padding: 4px 14px; border-radius: 16px; font-size: 13px; font-weight: 600; color: white; }
.b1 { background: #dc2626; }
.b2 { background: #d97706; }
.b3 { background: #16a34a; }
.section-header h2 { font-size: 18px; color: var(--green); }

/* Unified Card (all tiers) */
.card { background: white; border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 2px 8px rgba(45,80,22,0.06); margin-bottom: 24px; overflow: hidden; }
.t-card .hero { padding: 22px 26px; border-bottom: 1px solid var(--border); }
.t1-hero { background: linear-gradient(135deg, rgba(232,240,224,0.6), white); }
.t2-hero { background: linear-gradient(135deg, rgba(254,243,199,0.5), white); }
.t3-hero { background: linear-gradient(135deg, rgba(232,240,224,0.25), white); }
.t-card .eyebrow { font-size: 11px; color: var(--green); letter-spacing: 1px; opacity: 0.95; display: flex; align-items: center; gap: 8px; }
.t-card .eyebrow .badge { font-size: 11px; padding: 3px 10px; border-radius: 12px; }
.card-title { font-size: 21px; font-weight: 700; line-height: 1.4; margin: 10px 0 8px; color: var(--text); }
.meta-row { font-size: 13px; color: var(--text-muted); line-height: 1.6; }
.meta-row.meta-mini { font-size: 12px; margin-top: 4px; margin-bottom: 8px; }
.body { padding: 22px 26px; }
.h3 { font-size: 15px; font-weight: 600; color: var(--green); margin: 20px 0 10px; padding-left: 4px; border-left: 3px solid var(--green); padding-left: 10px; }
.h3:first-child { margin-top: 0; }
.body p { margin-bottom: 10px; font-size: 15px; }

/* Metaphor callout */
.metaphor-callout {
  background: var(--pink-light); border-left: 4px solid var(--pink);
  padding: 14px 18px; border-radius: 0 10px 10px 0; margin-bottom: 20px;
  font-size: 14px; line-height: 1.65; color: var(--text);
}

/* Features grid */
.features-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 14px 0 16px; }
.feat { background: var(--cream); border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; display: flex; gap: 12px; align-items: flex-start; transition: all 0.15s; }
.feat:hover { background: white; border-color: var(--green-mid); box-shadow: 0 2px 6px rgba(45,80,22,0.08); }
.feat-emoji { font-size: 22px; flex-shrink: 0; line-height: 1.2; }
.feat-body { flex: 1; }
.feat-title { font-size: 13px; font-weight: 600; color: var(--green); margin-bottom: 2px; }
.feat-desc { font-size: 12px; line-height: 1.5; color: var(--text-muted); }
.feat-text { font-size: 13px; line-height: 1.5; color: var(--text); }

/* SVG wrap */
.svg-wrap { background: #f8f9fa; border: 1px solid var(--border); border-radius: 8px; padding: 14px; margin: 16px 0; overflow-x: auto; text-align: center; }
.svg-wrap svg { max-width: 100%; height: auto; }
.svg-caption { font-size: 11px; color: var(--text-muted); margin-top: 8px; font-style: italic; }

/* Thoughts (引发思考) */
.thought {
  background: var(--green-pale); border-left: 4px solid var(--green);
  padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 8px 0;
  font-size: 14px; line-height: 1.65; position: relative; padding-left: 42px;
}
.thought-num {
  position: absolute; left: 14px; top: 12px; background: var(--green); color: white;
  width: 22px; height: 22px; border-radius: 50%; display: inline-flex;
  align-items: center; justify-content: center; font-size: 12px; font-weight: 700;
}
.thought-mini {
  background: var(--green-pale); border-left: 3px solid var(--green);
  padding: 8px 12px; border-radius: 0 6px 6px 0; margin: 6px 0;
  font-size: 13px; line-height: 1.55;
}
.value-mini { background: var(--cream); border-left: 3px solid var(--pink); padding: 8px 12px; border-radius: 0 6px 6px 0; margin: 8px 0; font-size: 13px; line-height: 1.55; }

/* Quiz details */
details.quiz { background: #f5f5f0; border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; margin: 16px 0; }
details.quiz summary { font-weight: 600; font-size: 14px; cursor: pointer; color: var(--green); list-style: none; }
details.quiz summary::-webkit-details-marker { display: none; }
details.quiz summary::before { content: "▸ "; color: var(--green-mid); transition: transform 0.2s; }
details.quiz[open] summary::before { content: "▾ "; }
.answer { background: var(--pink-light); border-left: 3px solid var(--pink); padding: 12px 16px; margin-top: 10px; font-size: 13px; line-height: 1.6; border-radius: 0 8px 8px 0; }
details.quiz-mini { padding: 8px 12px; margin: 6px 0; }
details.quiz-mini summary { font-size: 12px; }

/* Link row */
.link-row { display: flex; gap: 8px; padding: 14px 26px; border-top: 1px solid var(--border); background: #fafaf8; flex-wrap: wrap; }
.link-btn { padding: 6px 14px; background: white; border: 1px solid var(--border); border-radius: 16px; font-size: 12px; color: var(--green); text-decoration: none; transition: all 0.15s; }
.link-btn:hover { background: var(--green); color: white; }
.compact-link { font-size: 12px; color: var(--green-mid); text-decoration: none; display: inline-block; margin-top: 6px; }

/* Tier 2 grid */
.t2-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.t2-card { padding: 18px; }
.t2-head { margin-bottom: 8px; }
.tag-t2 { display: inline-block; background: var(--green-pale); color: var(--green); padding: 2px 10px; border-radius: 10px; font-size: 11px; font-weight: 600; margin-bottom: 6px; }
.t2-card h3 { font-size: 16px; font-weight: 700; line-height: 1.4; }
.t2-body { font-size: 13px; line-height: 1.6; color: var(--text); margin: 8px 0; }
.t2-body p { font-size: 13px; }

/* Tier 3 table */
.t3-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(45,80,22,0.06); }
.t3-table th { background: var(--green-pale); color: var(--green); padding: 10px 12px; text-align: left; font-size: 11px; text-transform: uppercase; }
.t3-table td { padding: 12px; border-bottom: 1px solid var(--border); font-size: 13px; vertical-align: top; }
.t3-table tr:last-child td { border-bottom: none; }
.t3-n { width: 80px; color: var(--green); font-weight: 600; white-space: nowrap; }
.t3-title { font-weight: 600; }
.t3-link a { color: var(--green-mid); text-decoration: none; font-size: 18px; }

/* Term tooltip */
.term { border-bottom: 1px dotted var(--green); cursor: pointer; position: relative; }
.term-popup {
  position: fixed; background: #2d2d2d; color: white;
  padding: 10px 14px; border-radius: 6px; max-width: 320px;
  font-size: 12px; line-height: 1.55; z-index: 2000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3); pointer-events: none;
}

/* Vault link */
.vault-link { color: var(--green-mid); text-decoration: none; font-weight: 500; }
.vault-link:hover { text-decoration: underline; }
.vault-link code { background: var(--green-pale); padding: 1px 6px; border-radius: 3px; font-size: 12px; color: var(--green); }

code { background: #f0ede4; padding: 1px 6px; border-radius: 3px; font-size: 13px; font-family: "SF Mono", Menlo, Consolas, monospace; }

@media (max-width: 880px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: relative; height: auto; }
  .features-grid, .t2-grid { grid-template-columns: 1fr; }
  .main { padding: 20px; }
}
'''

    today_main = frontmatter.get('today_main', '今日 AI 主线')

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Digest {date_str}</title>
<style>{css}</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="layout">
{sidebar}
<main class="main">
  <section class="page-hero">
    <div class="eyebrow">AI Builders Daily Digest</div>
    <h1>{date_str}</h1>
    <div class="subtitle">每日 AI 圈深度信号 · 个性化推荐 · 含 vault 命中</div>
    <div class="stats">
      <div class="stat-box"><span class="stat-num">{tier_counts[1]}</span><span class="stat-label">🔴 必读</span></div>
      <div class="stat-box"><span class="stat-num">{tier_counts[2]}</span><span class="stat-label">🟡 值得看</span></div>
      <div class="stat-box"><span class="stat-num">{tier_counts[3]}</span><span class="stat-label">🟢 背景信号</span></div>
    </div>
  </section>

  {f'<div class="section-header" id="sec-t1"><span class="badge b1">🔴 Tier 1</span><h2>必读 · {tier_counts[1]} 条</h2></div>{t1_html}' if t1_html else ''}

  {f'<div class="section-header" id="sec-t2"><span class="badge b2">🟡 Tier 2</span><h2>值得看 · {tier_counts[2]} 条</h2></div>{t2_grid}' if t2_grid else ''}

  {f'<div class="section-header" id="sec-t3"><span class="badge b3">🟢 Tier 3</span><h2>背景信号 · {tier_counts[3]} 条</h2></div>{t3_table}' if t3_table else ''}

  <footer style="margin: 40px 0 20px; padding: 16px 0; border-top: 1px solid var(--border); text-align: center; font-size: 12px; color: var(--text-muted);">
    daily-digest v9 · 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · <a href="https://github.com/wzm000001/personal-feed-system" target="_blank" style="color: var(--green-mid); text-decoration: none;">GitHub</a>
  </footer>
</main>
</div>

<div class="term-popup" id="termPopup" style="display:none"></div>

<script>
// Progress bar
const progressEl = document.getElementById('progress');
window.addEventListener('scroll', () => {{
  const h = document.documentElement;
  progressEl.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight) * 100) + '%';
}});

// Sidebar active link
const links = [...document.querySelectorAll('.sidebar a[data-id]')];
const targets = links.map(a => document.getElementById(a.dataset.id)).filter(Boolean);
if (targets.length) {{
  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        links.forEach(a => a.classList.toggle('active', a.dataset.id === entry.target.id));
      }}
    }});
  }}, {{ rootMargin: '-30% 0px -60% 0px' }});
  targets.forEach(t => observer.observe(t));
}}

// Term tooltip
const popup = document.getElementById('termPopup');
document.querySelectorAll('.term').forEach(term => {{
  term.addEventListener('mouseenter', e => {{
    popup.textContent = term.dataset.def;
    const r = term.getBoundingClientRect();
    const popupW = Math.min(320, term.dataset.def.length * 14);
    popup.style.left = Math.min(r.left, window.innerWidth - popupW - 20) + 'px';
    popup.style.top = (r.bottom + 6) + 'px';
    popup.style.display = 'block';
  }});
  term.addEventListener('mouseleave', () => {{
    popup.style.display = 'none';
  }});
}});
</script>
</body>
</html>
'''


# ============ Main ============

def main():
    if len(sys.argv) < 2:
        print("用法: python3 render-html.py <reading-log-md-path> [<output-html-path>]", file=sys.stderr)
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"❌ md 文件不存在: {md_path}", file=sys.stderr)
        sys.exit(2)

    out_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else md_path.with_suffix('.html')

    text = md_path.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(text)
    articles = parse_articles(body)

    # 尝试加载 extras.json (LLM 写入的高质量 metaphor / features / flow)
    extras_path = md_path.with_suffix('.extras.json')
    extras = {}
    if extras_path.exists():
        import json
        try:
            extras = json.loads(extras_path.read_text(encoding='utf-8'))
            print(f"📥 加载 extras.json: {len(extras)} 个 article 有 enhance 数据")
        except Exception as e:
            print(f"⚠️ extras.json 解析失败: {e}, 降级", file=sys.stderr)

    # 合并 extras 到 article
    for art in articles:
        ex = extras.get(art['id'])
        if ex:
            art['metaphor_extra'] = ex.get('metaphor')
            # extras 的 features 优先 (高质量 dict 结构)
            if ex.get('features'):
                art['features'] = ex['features']
            if ex.get('flow'):
                art['flow'] = ex['flow']

    html_out = render_html(fm, articles)
    out_path.write_text(html_out, encoding='utf-8')

    print(f"✅ 已生成: {out_path} ({len(html_out)} bytes, {len(articles)} 篇)")
    # 统计
    by_tier = {}
    for a in articles:
        by_tier[a['tier']] = by_tier.get(a['tier'], 0) + 1
    print(f"   Tier 分布: {by_tier}")


if __name__ == '__main__':
    main()

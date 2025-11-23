# config.py - Agent 的规则与配置中心

# --- 1. 智能分类标准 (Taxonomy) ---
CATEGORIES = [
    "🤖 大语言模型 (LLMs)",
    "🛠️ 编程与开发工具 (DevTools)",
    "🎨 视觉与多媒体创作 (Vision/Audio)",
    "⚡ 智能体与自动化 (Agents)",
    "📝 生产力与办公 (Productivity)",
    "📰 行业深度与大V观点 (Insights)",
    "🔬 硬核研究与论文 (Research)"
]

# --- 2. 监测源列表 (Sensors) ---
# GitHub 和 HF 是自动抓取热榜，这里主要配置 RSS 源
RSS_FEEDS = {
    # == 顶流大V/官方博客 ==
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/feed",
    "Google DeepMind": "https://deepmind.google/blog/rss.xml",
    "Andrej Karpathy": "https://karpathy.github.io/feed.xml",
    "Paul Graham": "http://www.aaronsw.com/2002/feeds/pgessays.rss",
    
    # == 商业新品/技术媒体 ==
    "Product Hunt": "https://www.producthunt.com/feed",
    "Hacker News": "http://hnrss.org/best", 
    "The Verge AI": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
}

# --- 3. DeepSeek 思考指令 (System Prompt) ---
# 核心差异化：强制要求提取“迭代亮点”和“使用教程”
AGENT_PROMPT = """
你是一个专业的 AI 深度情报分析师。
请阅读以下原始情报：
【标题】：{title}
【来源】：{source}
【内容】：{content}
【链接】：{link}

任务要求：
1. **真实性判断**：如果是广告、简单的 Bug 修复、或者非 AI 内容，标记为 invalid。
2. **分类**：从以下列表选一个最贴切的：{categories}。
3. **深度提取**：
    - **中文标题**：通俗易懂。
    - **迭代亮点**：相比旧版或竞品，它强在哪里？(核心卖点)。
    - **创作者案例**：具体谁可以用它做什么？(例如：插画师可用它生成...)。
    - **AI速成指南**：基于已有信息，总结 3 步以内的上手步骤 (Step-by-step)。如果不清楚，根据功能推测通用步骤。

请返回严格的 JSON 格式：
{{
    "is_valid": true,
    "category": "...",
    "cn_title": "...",
    "update_highlight": "...",
    "use_case": "...",
    "ai_tutorial": ["步骤1...", "步骤2...", "步骤3..."],
    "score": 85
}}
"""

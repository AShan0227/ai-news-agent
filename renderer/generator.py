import os
import json
import datetime
import sys
import urllib.parse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def render_html(data, insights):
    print("🎨 [UI引擎] 正在渲染 V3.0 赛博仪表盘...")
    
    grouped = {}
    for item in data:
        cat = item.get("category", "未分类")
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(item)

    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 深度情报 V3.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
            body {{ background-color: #0b0f19; color: #e2e8f0; font-family: 'Inter', sans-serif; }}
            @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            .animate-card {{ animation: fadeInUp 0.6s ease-out forwards; opacity: 0; }}
            .cyber-card {{ background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(15, 23, 42, 0.6)); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
            .cyber-card:hover {{ border-color: rgba(59, 130, 246, 0.5); box-shadow: 0 0 20px rgba(59, 130, 246, 0.2); transform: translateY(-5px); }}
            .category-banner {{ background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(0,0,0,0) 100%); border-left: 4px solid #3b82f6; }}
        </style>
    </head>
    <body class="min-h-screen p-4 md:p-8">
        <header class="max-w-7xl mx-auto mb-12 flex justify-between items-end border-b border-slate-800 pb-6">
            <div>
                <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight mb-2">
                    AI HUNTER <span class="text-xs text-slate-500 font-mono border border-slate-700 px-2 py-1 rounded ml-2">V3.0 LIVE</span>
                </h1>
                <p class="text-slate-400 text-sm">全网深度情报监测 / 自动研判 / 实时更新</p>
            </div>
            <div class="text-right hidden md:block">
                <div class="text-3xl font-mono font-bold text-white">{datetime.datetime.now().strftime('%H:%M')}</div>
                <div class="text-xs text-slate-500 uppercase tracking-widest">{datetime.datetime.now().strftime('%Y-%m-%d')}</div>
            </div>
        </header>

        <main class="max-w-7xl mx-auto space-y-16">
    """

    delay_counter = 0
    for cat, items in grouped.items():
        if not items: continue
        # 如果 main.py 还没传参 insights，这里做个兼容处理
        insight_text = insights.get(cat, "该领域今日运行平稳。") if insights else "该领域今日运行平稳。"
        
        html += f"""
        <section>
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-white flex items-center gap-3 mb-3">
                    <i class="fa-solid fa-layer-group text-blue-500"></i> {cat}
                    <span class="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded-full">{len(items)}</span>
                </h2>
                <div class="category-banner p-4 rounded-r-lg">
                    <p class="text-sm text-blue-200 italic font-medium"><i class="fa-solid fa-quote-left mr-2 opacity-50"></i>{insight_text}</p>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        """
        
        for item in items:
            search_q = urllib.parse.quote(f"{item.get('title')} tutorial guide")
            tutorial_link = f"https://www.youtube.com/results?search_query={search_q}"
            delay_style = f"animation-delay: {delay_counter * 100}ms"
            delay_counter += 1
            ts = item.get('timestamp', '刚刚')
            
            card = f"""
                <article class="cyber-card rounded-xl p-5 flex flex-col h-full transition-all duration-300 animate-card" style="{delay_style}">
                    <div class="flex justify-between items-start mb-4">
                        <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-slate-800 text-slate-400 border border-slate-700">{item.get('source','Web')}</span>
                        <div class="flex items-center gap-2 text-[10px] text-slate-500 font-mono"><i class="fa-regular fa-clock"></i> {ts}</div>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-3 leading-snug hover:text-blue-400 transition"><a href="{item['link']}" target="_blank">{item.get('cn_title', item['title'])}</a></h3>
                    <div class="space-y-3 flex-grow">
                        <div class="bg-slate-900/50 p-3 rounded border-l-2 border-amber-500">
                            <div class="text-[10px] text-amber-500 uppercase font-bold mb-1">⚡ 核心亮点</div>
                            <p class="text-xs text-slate-300 leading-relaxed">{item.get('update_highlight', '暂无分析')}</p>
                        </div>
                        <div class="bg-slate-900/50 p-3 rounded border-l-2 border-emerald-500">
                            <div class="text-[10px] text-emerald-500 uppercase font-bold mb-1">🎨 创作者用法</div>
                            <p class="text-xs text-slate-300 leading-relaxed">{item.get('use_case', '暂无案例')}</p>
                        </div>
                    </div>
                    <div class="mt-5 pt-4 border-t border-slate-800/50 grid grid-cols-2 gap-3">
                        <a href="{item['link']}" target="_blank" class="flex items-center justify-center gap-2 py-2 rounded bg-slate-800 text-xs font-bold text-slate-300 hover:bg-slate-700 transition"><i class="fa-solid fa-link"></i> 原文</a>
                        <a href="{tutorial_link}" target="_blank" class="flex items-center justify-center gap-2 py-2 rounded bg-blue-600/20 text-xs font-bold text-blue-400 hover:bg-blue-600 hover:text-white transition"><i class="fa-brands fa-youtube"></i> 找教程</a>
                    </div>
                </article>
            """
            html += card
        html += "</div></section>"
    html += "</main><footer class='max-w-7xl mx-auto mt-20 py-8 border-t border-slate-800 text-center text-slate-600 text-xs font-mono'>AGENT V3.0 • DEEPSEEK INSIDE</footer></body></html>"
    
    os.makedirs("data/report", exist_ok=True)
    with open("data/report/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("🎉 V3.0 赛博网页生成完毕！")

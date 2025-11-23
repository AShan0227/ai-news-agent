import os
import json
import datetime
import sys
import urllib.parse

# 引用父目录配置
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def render_html(data):
    print("🎨 [UI引擎] 正在渲染 V2.0 暗黑仪表盘...")
    
    # 1. 统计数据
    total_items = len(data)
    high_score_items = len([i for i in data if i.get('score', 0) > 85])
    
    # 2. 按分类分组
    grouped = {}
    for item in data:
        cat = item.get("category", "未分类")
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(item)

    # HTML 头部 (引入了 Chart.js 做图表，FontAwesome 做图标)
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN" class="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 猎人终极仪表盘</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <script>
            tailwind.config = {{
                darkMode: 'class',
                theme: {{ extend: {{ colors: {{ gray: {{ 900: '#111827', 800: '#1f2937', 700: '#374151' }} }} }} }}
            }}
        </script>
        <style>
            body {{ background-color: #0f172a; color: #e2e8f0; font-family: 'Segoe UI', Roboto, sans-serif; }}
            .glass-panel {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
            .neon-text {{ text-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }}
        </style>
    </head>
    <body class="min-h-screen p-6">
        
        <div class="flex justify-between items-center mb-8">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <i class="fa-solid fa-brain text-2xl text-white"></i>
                </div>
                <div>
                    <h1 class="text-2xl font-bold text-white tracking-wider">AI HUNTER <span class="text-blue-500">V2.0</span></h1>
                    <p class="text-xs text-slate-400">全网实时情报监测系统 | 在线</p>
                </div>
            </div>
            <div class="flex gap-4">
                <div class="glass-panel px-4 py-2 rounded-lg text-center">
                    <div class="text-xs text-slate-400">上次扫描</div>
                    <div class="font-mono text-emerald-400">{datetime.datetime.now().strftime('%H:%M')}</div>
                </div>
                <div class="glass-panel px-4 py-2 rounded-lg text-center">
                    <div class="text-xs text-slate-400">情报总数</div>
                    <div class="font-bold text-white">{total_items}</div>
                </div>
            </div>
        </div>

        <div class="mb-8 bg-black rounded-xl p-4 font-mono text-xs border border-slate-800 h-32 overflow-y-auto opacity-80">
            <div class="text-green-500">>> SYSTEM INITIALIZED...</div>
            <div class="text-slate-400">>> Connecting to Google News Network... OK</div>
            <div class="text-slate-400">>> DeepSeek Analysis Module... ACTIVATED</div>
            <div class="text-blue-400">>> Filtering items based on relevance score...</div>
            <div class="text-white animate-pulse">>> WAITING FOR NEXT CYCLE...</div>
        </div>

        <div class="space-y-12">
    """

    for cat, items in grouped.items():
        if not items: continue
        html += f"""
        <div class="category-section">
            <h2 class="text-xl font-bold mb-4 flex items-center text-white border-l-4 border-blue-500 pl-3">
                {cat} <span class="ml-3 text-xs bg-slate-700 px-2 py-0.5 rounded text-slate-300">{len(items)}</span>
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        """
        
        for item in items:
            # 智能深链构建：如果没有教程，就生成一个 Google/YouTube 搜索链接
            search_q = urllib.parse.quote(f"{item.get('title')} tutorial guide")
            tutorial_link = f"https://www.youtube.com/results?search_query={search_q}"
            
            # 分数颜色
            score = item.get('score', 0)
            score_color = "text-green-400" if score > 80 else "text-slate-400"

            card = f"""
                <div class="glass-panel rounded-xl overflow-hidden hover:border-blue-500/50 transition duration-300 flex flex-col group">
                    <div class="p-5 flex-grow">
                        <div class="flex justify-between items-start mb-3">
                            <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-slate-700 text-slate-300">{item.get('source','Web')}</span>
                            <span class="font-mono text-sm font-bold {score_color}">Score: {score}</span>
                        </div>
                        
                        <h3 class="text-lg font-bold mb-2 text-white group-hover:text-blue-400 transition leading-snug">
                            <a href="{item['link']}" target="_blank">{item.get('cn_title', item['title'])}</a>
                        </h3>
                        
                        <div class="mt-4 space-y-3">
                            <div class="bg-slate-800/50 p-3 rounded border border-slate-700/50">
                                <div class="text-[10px] text-blue-400 uppercase font-bold mb-1">⚡ 核心亮点</div>
                                <p class="text-sm text-slate-300">{item.get('update_highlight', '暂无分析')}</p>
                            </div>
                            
                            <div class="bg-slate-800/50 p-3 rounded border border-slate-700/50">
                                <div class="text-[10px] text-emerald-400 uppercase font-bold mb-1">💡 创作者能做什么</div>
                                <p class="text-sm text-slate-300">{item.get('use_case', '暂无案例')}</p>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-2 divide-x divide-slate-700 border-t border-slate-700">
                        <a href="{item['link']}" target="_blank" class="py-3 text-center text-xs font-bold text-slate-400 hover:text-white hover:bg-slate-700 transition">
                            📄 原文链接
                        </a>
                        <a href="{tutorial_link}" target="_blank" class="py-3 text-center text-xs font-bold text-slate-400 hover:text-yellow-400 hover:bg-slate-700 transition flex items-center justify-center gap-1">
                            <i class="fa-brands fa-youtube"></i> 找教程
                        </a>
                    </div>
                </div>
            """
            html += card
        html += "</div></div>"

    html += "</div></body></html>"
    
    os.makedirs("data/report", exist_ok=True)
    with open("data/report/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("🎉 V2.0 仪表盘生成完毕！")

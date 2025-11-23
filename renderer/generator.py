import os
import json
import datetime
import sys
import urllib.parse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def render_html(data, insights):
    print("🎨 [UI引擎] 正在渲染 V4.0 头条版...")
    
    # 获取头条数据
    top_picks = insights.get('top_picks', [])
    daily_summary = insights.get('daily_summary', '正在分析今日趋势...')
    
    # 分组
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
        <title>AI 深度情报 V4.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
            body {{ background-color: #050505; color: #e2e8f0; font-family: 'Inter', sans-serif; }}
            .glass {{ background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); }}
            .hero-gradient {{ background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); }}
            .glow-text {{ text-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }}
        </style>
    </head>
    <body class="min-h-screen pb-20">
        
        <div class="bg-slate-900 border-b border-slate-800 sticky top-0 z-50 bg-opacity-90 backdrop-blur">
            <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
                <div class="flex items-center gap-3">
                    <i class="fa-solid fa-bolt text-yellow-400 text-xl animate-pulse"></i>
                    <h1 class="text-xl font-bold tracking-tight text-white">AI HUNTER <span class="text-xs bg-blue-600 px-2 py-0.5 rounded ml-2">LIVE</span></h1>
                </div>
                <div class="text-xs text-slate-400 font-mono hidden md:block">
                    最后更新: {datetime.datetime.now().strftime('%H:%M')} | 源: Google/GitHub/HF
                </div>
            </div>
        </div>

        <main class="max-w-7xl mx-auto px-4 mt-8 space-y-12">
            
            <section class="hero-gradient rounded-3xl p-8 shadow-2xl border border-indigo-900/50">
                <div class="mb-8">
                    <h2 class="text-3xl font-extrabold text-white mb-4 glow-text">今日重点关注</h2>
                    <p class="text-lg text-indigo-200 leading-relaxed max-w-3xl">"{daily_summary}"</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    """
    
    # 渲染 Top 3
    for item in top_picks:
        search_q = urllib.parse.quote(f"{item.get('title')} tutorial")
        html += f"""
            <div class="bg-slate-900/80 rounded-xl p-6 border border-indigo-500/30 hover:border-indigo-400 transition hover:-translate-y-1 relative overflow-hidden group">
                <div class="absolute top-0 right-0 bg-indigo-600 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">SCORE: {item.get('score')}</div>
                <div class="text-indigo-400 text-xs font-bold uppercase mb-2 tracking-wider">{item.get('category')}</div>
                <h3 class="text-xl font-bold text-white mb-3 leading-tight group-hover:text-indigo-300">
                    <a href="{item['link']}" target="_blank">{item.get('cn_title')}</a>
                </h3>
                <p class="text-sm text-slate-400 mb-4 line-clamp-3">{item.get('update_highlight')}</p>
                <div class="flex gap-2">
                    <a href="{item['link']}" target="_blank" class="flex-1 text-center bg-white text-slate-900 py-2 rounded-lg text-xs font-bold hover:bg-indigo-50">原文</a>
                    <a href="https://www.youtube.com/results?search_query={search_q}" target="_blank" class="flex-1 text-center bg-indigo-600 text-white py-2 rounded-lg text-xs font-bold hover:bg-indigo-500">看教程</a>
                </div>
            </div>
        """

    html += """
                </div>
            </section>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
    """
    
    # 侧边栏导航
    html += """<div class="hidden md:block col-span-1 space-y-2 sticky top-24 h-fit">
                <h3 class="text-xs font-bold text-slate-500 uppercase mb-4">频道导航</h3>"""
    for cat in grouped.keys():
        html += f"""<a href="#{cat}" class="block text-sm text-slate-300 hover:text-white hover:pl-2 transition-all py-1">{cat}</a>"""
    html += "</div>"

    # 主内容区
    html += "<div class='col-span-1 md:col-span-3 space-y-16'>"
    
    for cat, items in grouped.items():
        html += f"""
        <section id="{cat}" class="scroll-mt-24">
            <h3 class="text-xl font-bold text-white flex items-center gap-3 mb-6 border-b border-slate-800 pb-2">
                <span class="w-2 h-6 bg-blue-600 rounded-full"></span> {cat}
            </h3>
            <div class="grid grid-cols-1 gap-4">
        """
        for item in items:
            # 普通列表样式 (比头条稍微简化一点)
            html += f"""
                <div class="glass rounded-lg p-5 hover:bg-slate-800/50 transition flex flex-col sm:flex-row gap-4 items-start">
                    <div class="flex-grow">
                        <div class="flex items-center gap-2 mb-1">
                            <span class="text-[10px] border border-slate-700 text-slate-400 px-1.5 rounded">{item.get('source')}</span>
                            <span class="text-[10px] text-slate-500">{item.get('timestamp')}</span>
                        </div>
                        <h4 class="text-lg font-bold text-slate-200 hover:text-blue-400 mb-2">
                            <a href="{item['link']}" target="_blank">{item.get('cn_title')}</a>
                        </h4>
                        <p class="text-sm text-slate-400 mb-3">{item.get('update_highlight')}</p>
                        <div class="bg-slate-900/50 p-2 rounded border-l-2 border-emerald-500 text-xs text-slate-300">
                            <span class="text-emerald-500 font-bold mr-1">用法:</span> {item.get('use_case')}
                        </div>
                    </div>
                    <div class="sm:w-32 flex-shrink-0 flex flex-col gap-2">
                         <a href="{item['link']}" target="_blank" class="block w-full text-center border border-slate-700 text-slate-400 py-1.5 rounded text-xs hover:text-white hover:border-slate-500">阅读</a>
                         <a href="https://www.youtube.com/results?search_query={urllib.parse.quote(item.get('title') + ' tutorial')}" target="_blank" class="block w-full text-center bg-blue-600/10 text-blue-400 py-1.5 rounded text-xs hover:bg-blue-600 hover:text-white transition">教程</a>
                    </div>
                </div>
            """
        html += "</div></section>"

    html += """
            </div>
        </div>
        </main>
    </body>
    </html>
    """
    
    os.makedirs("data/report", exist_ok=True)
    with open("data/report/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("🎉 V4.0 头条版生成完毕！")

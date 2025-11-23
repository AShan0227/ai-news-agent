import feedparser
import ssl
import urllib.parse
import sys
import os

# 解决 SSL 问题
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def search_google_news(keyword):
    """主动去 Google News 搜索过去 24 小时的头条"""
    print(f"🕵️‍♂️ [猎人] 正在全网搜索: {keyword}...")
    try:
        encoded_query = urllib.parse.quote(f"{keyword} when:1d")
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        items = []
        seen_titles = set()
        
        for entry in feed.entries[:8]: 
            title = entry.title
            if title in seen_titles: continue
            seen_titles.add(title)
            if len(title) < 10: continue
            
            items.append({
                "source": "GoogleNews",
                "query": keyword,
                "title": title,
                "content": entry.get('summary', title),
                "link": entry.link,
                "timestamp": entry.published
            })
        return items
    except Exception as e:
        print(f"❌ 搜索 {keyword} 失败: {e}")
        return []

def get_data():
    all_items = []
    # === 定义你的狩猎目标 ===
    targets = [
        "latest AI model release",   # 抓 GPT-5, Gemini 3
        "new AI coding agent",       # 抓 Devin, Cursor 类
        "text to video AI tool",     # 抓 Sora 2, Kling 类
        "AI tutorial guide how-to",  # 抓教程
        "Andrej Karpathy",           # 抓大佬动态
    ]
    
    for t in targets:
        items = search_google_news(t)
        all_items.extend(items)
        
    print(f"✅ [猎人] 共捕获 {len(all_items)} 条实时情报")
    return all_items

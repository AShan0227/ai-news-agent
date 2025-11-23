import os
import json
import sys
from openai import OpenAI
import datetime

# 动态添加路径以导入 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def analyze_items(raw_items):
    print(f"🧠 [Agent Core] 收到 {len(raw_items)} 条原始情报...")
    enriched_items = []
    
    # 1. 逐条深度分析
    for i, item in enumerate(raw_items):
        print(f"   [{i+1}/{len(raw_items)}] 分析: {item['title'][:20]}...")
        if 'timestamp' not in item:
            item['timestamp'] = datetime.datetime.now().strftime("%H:%M")

        prompt = config.AGENT_PROMPT.format(
            title=item['title'],
            source=item['source'],
            content=item['content'],
            link=item['link'],
            categories=json.dumps(config.CATEGORIES, ensure_ascii=False)
        )
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            ai_data = json.loads(response.choices[0].message.content)
            
            if ai_data.get("is_valid", False):
                item.update(ai_data)
                enriched_items.append(item)
        except Exception as e:
            print(f"      ❌ 单条分析失败: {e}")
            continue

    # 2. 生成【分类综述】(V3.0 新增功能)
    print("🧠 [Agent Core] 正在生成分类综述...") # <--- 刚才日志里缺了这句话
    
    grouped = {}
    for item in enriched_items:
        cat = item.get("category", "其他")
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(item['cn_title'])
    
    category_insights = {}
    
    for cat, titles in grouped.items():
        if len(titles) < 1: continue
        summary_prompt = f"你是AI主编。今天在【{cat}】领域发生了这些事：{json.dumps(titles, ensure_ascii=False)}。请用一句话犀利地点评今天的该领域的趋势或重点（50字以内）。"
        try:
            res = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": summary_prompt}]
            )
            category_insights[cat] = res.choices[0].message.content
        except: pass

    # 返回两个值
    return enriched_items, category_insights

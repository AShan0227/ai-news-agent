import os
import json
import sys
from openai import OpenAI
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def analyze_items(raw_items):
    print(f"🧠 [Agent Core] 收到 {len(raw_items)} 条原始情报...")
    enriched_items = []
    
    # 1. 深度分析每一条
    for i, item in enumerate(raw_items):
        if 'timestamp' not in item:
            item['timestamp'] = datetime.datetime.now().strftime("%H:%M")

        # 这里的 Prompt 微调过，强调让 AI 评分 (score)
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
                # === 关键逻辑：权重调整 ===
                # 你强调要关注“新工具”和“应用”，所以给这两类加分
                final_score = ai_data.get('score', 70)
                cat = ai_data.get('category', '')
                
                # 如果是工具类，强制加分，确保它们能上头条
                if "工具" in cat or "创作" in cat or "模型" in cat or "Agent" in cat:
                    final_score += 15 
                
                ai_data['score'] = min(final_score, 100) # 封顶100
                
                item.update(ai_data)
                enriched_items.append(item)
        except: continue

    # 2. 生成分类综述
    grouped = {}
    for item in enriched_items:
        cat = item.get("category", "其他")
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(item['cn_title'])
    
    category_insights = {}
    for cat, titles in grouped.items():
        if len(titles) < 1: continue
        try:
            prompt = f"一句话总结今天【{cat}】领域的动态：{json.dumps(titles, ensure_ascii=False)}"
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
            category_insights[cat] = res.choices[0].message.content
        except: pass

    # 3. 选出【今日头条】(Top 3)
    # 按照分数排序，取前3名
    enriched_items.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_picks = enriched_items[:3]
    
    # 让 AI 为这 3 个写一段总的“日报摘要”
    daily_summary = "今日平稳运行。"
    if top_picks:
        try:
            top_titles = [x['cn_title'] for x in top_picks]
            summary_prompt = f"""
            你是 AI 情报官。请根据今天最重要的这三件事写一段简报（100字以内），开头要吸引人，告诉用户为什么今天很特别：
            {json.dumps(top_titles, ensure_ascii=False)}
            """
            res = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": summary_prompt}])
            daily_summary = res.choices[0].message.content
        except: pass

    # 将 summary 塞进 insights 字典里传给前端
    category_insights['daily_summary'] = daily_summary
    category_insights['top_picks'] = top_picks # 把头条单独传过去

    return enriched_items, category_insights

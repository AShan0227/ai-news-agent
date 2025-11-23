import os
import json
import sys
from openai import OpenAI

# 动态添加路径以导入 config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# 初始化 DeepSeek 客户端
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def analyze_items(raw_items):
    print(f"🧠 [Agent Core] 收到 {len(raw_items)} 条原始情报，开始深度研判...")
    
    enriched_items = []
    
    for i, item in enumerate(raw_items):
        print(f"   [{i+1}/{len(raw_items)}] 正在分析: {item['title'][:20]}...")
        
        # 1. 填充 Prompt 模板
        prompt = config.AGENT_PROMPT.format(
            title=item['title'],
            source=item['source'],
            content=item['content'],
            link=item['link'],
            categories=json.dumps(config.CATEGORIES, ensure_ascii=False)
        )
        
        try:
            # 2. 调用 DeepSeek
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            
            # 3. 解析结果
            content = response.choices[0].message.content
            # 有时候 AI 会带 markdown 标记，保险起见去掉
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
                
            ai_data = json.loads(content)
            
            # 4. 只有判定为有效的才收录
            if ai_data.get("is_valid", False):
                # 合并数据
                item.update(ai_data)
                enriched_items.append(item)
                print(f"      ✅ 收录: {ai_data['cn_title']}")
            else:
                print(f"      🗑️ 过滤: 无效/低价值内容")
                
        except Exception as e:
            print(f"      ❌ 分析出错: {e}")
            continue
            
    return enriched_items

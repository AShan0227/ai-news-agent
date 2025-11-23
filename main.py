import os
import sys

from sources import github_source, huggingface_source, rss_source
from core import analyst
from renderer import generator

def main():
    print("\n" + "="*50)
    print("   🤖 AI Deep Agent V3.0 - Cloud Edition")
    print("="*50 + "\n")
    
    # 检查密钥
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 错误: 未设置 DEEPSEEK_API_KEY")
        exit(1)

    # 1. 全域感知
    all_data = []
    try: all_data.extend(github_source.get_data())
    except Exception as e: print(f"⚠️ GitHub 源跳过: {e}")
    
    try: all_data.extend(huggingface_source.get_data())
    except Exception as e: print(f"⚠️ HF 源跳过: {e}")
    
    try: all_data.extend(rss_source.get_data())
    except Exception as e: print(f"⚠️ RSS 源跳过: {e}")
    
    if not all_data:
        print("⚠️ 未采集到数据，退出。")
        return

    # 2. 深度思考 (⚠️ 必须接收两个返回值!)
    enriched_data, category_insights = analyst.analyze_items(all_data)
    
    # 3. 结果展示 (传入两个参数)
    generator.render_html(enriched_data, category_insights)
    
    print("\n🚀 云端运行完毕！")

if __name__ == "__main__":
    main()

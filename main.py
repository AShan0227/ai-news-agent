import os
import sys

from sources import github_source, huggingface_source, rss_source
from core import analyst
from renderer import generator

def main():
    print("\n" + "="*50)
    print("   🤖 AI Deep Agent V2.0 - 全网深度情报系统")
    print("="*50 + "\n")
    
    # 0. 检查 Key
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 错误: 未设置 DEEPSEEK_API_KEY")
        return

    # 1. 全域感知 (Collection)
    # 注意：rss_source 现在是全网猎人，会抓很久，请耐心等待
    all_data = []
    all_data.extend(github_source.get_data())
    all_data.extend(huggingface_source.get_data())
    all_data.extend(rss_source.get_data()) 
    
    if not all_data:
        print("⚠️ 未采集到数据，请检查网络。")
        return

    # 2. 深度思考 (Analysis)
    enriched_data = analyst.analyze_items(all_data)
    
    # 3. 结果展示 (Rendering)
    generator.render_html(enriched_data)
    
    # 4. 自动打开
    print("\n🚀 系统运行完毕！正在打开仪表盘...")
    os.system("open data/report/index.html")

if __name__ == "__main__":
    main()

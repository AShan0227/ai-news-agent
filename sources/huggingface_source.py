from huggingface_hub import list_spaces

def get_data():
    print("🤗 [HuggingFace] 正在扫描热门 Space...")
    try:
        spaces = list_spaces(sort="likes7d", limit=5)
        items = []
        for s in spaces:
            items.append({
                "source": "HuggingFace",
                "title": s.id,
                "content": f"HF Trending Space. Likes: {s.likes}. Author: {s.author}",
                "link": f"https://huggingface.co/spaces/{s.id}"
            })
        return items
    except Exception as e:
        print(f"❌ HF 扫描失败: {e}")
        return []

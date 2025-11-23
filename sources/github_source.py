import requests
from bs4 import BeautifulSoup

def get_data():
    print("📡 [GitHub] 正在扫描热榜...")
    try:
        url = "https://github.com/trending?since=daily"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(resp.text, "lxml")
        repos = soup.find_all("article", class_="Box-row")
        
        items = []
        for repo in repos:
            h2 = repo.find("h2") or repo.find("h1")
            link = "https://github.com" + h2.find("a")["href"]
            desc_tag = repo.find("p", class_="col-9")
            desc = desc_tag.text.strip() if desc_tag else "无简介"
            
            # 简单初筛
            if any(k in (link+desc).lower() for k in ['ai', 'gpt', 'llm', 'agent', 'model', 'diffusion']):
                items.append({
                    "source": "GitHub",
                    "title": link.split("/")[-1],
                    "content": desc,
                    "link": link
                })
        return items[:6] # 取前6个精品
    except Exception as e:
        print(f"❌ GitHub 扫描失败: {e}")
        return []

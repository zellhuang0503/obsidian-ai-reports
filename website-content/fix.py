import os
import re

folder = r"E:\CascadeProjects\vae_new_website\src\content\ai-daily-brief"

for filename in os.listdir(folder):
    if not filename.endswith(".mdx") or filename.endswith(".bak"):
        continue
    
    filepath = os.path.join(folder, filename)
    date = filename.replace("ai-daily-brief-", "").replace(".mdx", "")
    
    print(f"📝 處理: {filename}")
    
    # 讀取檔案 (UTF-8)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 備份原內容
    with open(filepath + '.bak2', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 1. 替換 date -> publishedAt
    content = re.sub(r'^date:', 'publishedAt:', content, flags=re.MULTILINE)
    
    # 2. 替換 description -> excerpt
    content = re.sub(r'^description:', 'excerpt:', content, flags=re.MULTILINE)
    
    # 3. 添加 slug（在 publishedAt 後面）
    if 'slug:' not in content:
        content = re.sub(r'(publishedAt:.*?\n)', r'\1slug: "' + date + '"\n', content)
    
    # 4. 添加 author AI Agent（在 slug 後面）
    if 'author:' not in content:
        content = re.sub(r'(slug:.*?\n)', r'\1author: "AI Agent"\n', content)
    else:
        # 如果已有 author，替換為 AI Agent
        content = re.sub(r'^author:.*$', 'author: "AI Agent"', content, flags=re.MULTILINE)
    
    # 5. 添加 categories（在 author 後面）
    if 'categories:' not in content:
        content = re.sub(r'(author:.*?\n)', r'\1categories: ["AI", "科技"]\n', content)
    
    # 寫回檔案 (UTF-8)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ 已修復")

print("")
print("🎉 全部完成！作者統一為 AI Agent")

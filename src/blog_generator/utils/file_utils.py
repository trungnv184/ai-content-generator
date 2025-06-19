import os
from datetime import datetime

def save_blog_post(content: str, output_dir: str, topic: str) -> str:
    timestamp = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    file_name = f"{timestamp}_{topic}_blog_post.md"
    file_path = os.path.join(output_dir, file_name )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Blog post saved to {file_path}")
    
    return file_path
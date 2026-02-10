import os
import json
from datetime import datetime
from string import Template

BASE_URL = "https://juhyoung0605.github.io"
POSTS_DIR = "posts"

POST_TEMPLATE_FILE = "post.html"
POST_DATA_FILE = "posts_data.json"

os.makedirs(POSTS_DIR, exist_ok=True)

def load_template():
    with open(POST_TEMPLATE_FILE, "r", encoding="utf-8") as f:
        return Template(f.read())

def load_posts():
    with open(POST_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_post(post, template):
    slug = post["slug"]
    filename = f"{slug}.html"
    url = f"{BASE_URL}/posts/{filename}"

    html = template.safe_substitute(
        title=post["title"],
        description=post.get("description", post["title"]),
        keywords=", ".join(post.get("keywords", [])),
        date=post["date"],
        content=post["content"],
        url=url
    )

    with open(os.path.join(POSTS_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)

    return url, post["date"]

def generate_index(posts):
    items = []
    for p in posts:
        items.append(
            f"<li><a href='/posts/{p['slug']}.html'>{p['title']}</a> <small>{p['date']}</small></li>"
        )

    html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Juhyoung Blog</title>
  <meta name="description" content="반도체, AI, 기술 블로그">
</head>
<body>
  <h1>📘 Juhyoung Blog</h1>
  <ul>
    {''.join(items)}
  </ul>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def generate_sitemap(urls):
    items = []
    for url, date in urls:
        items.append(f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{date}</lastmod>
  </url>
""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{BASE_URL}</loc>
    <lastmod>{datetime.now().date()}</lastmod>
  </url>
  {''.join(items)}
</urlset>
"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)

def main():
    template = load_template()
    posts = load_posts()

    sitemap_urls = []

    for post in posts:
        url, date = generate_post(post, template)
        sitemap_urls.append((url, date))

    generate_index(posts)
    generate_sitemap(sitemap_urls)

    print("✅ Blog updated successfully")

if __name__ == "__main__":
    main()

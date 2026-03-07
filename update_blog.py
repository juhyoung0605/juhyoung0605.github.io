import requests
import xml.etree.ElementTree as ET
import re
from datetime import datetime

RSS_URL = "https://rss.blog.naver.com/jubro_0605.xml"
SITE_URL = "https://juhyoung0605.github.io"

INDEX_FILE = "index.html"
SITEMAP_FILE = "sitemap.xml"

POST_LIMIT = 10


def clean_text(text):
    text = re.sub("<.*?>", "", text)
    text = text.replace("\n", " ").strip()
    return text[:120] + "…" if len(text) > 120 else text


print("📡 RSS 가져오는 중...")

res = requests.get(RSS_URL)
root = ET.fromstring(res.text)

posts = []

for item in root.findall(".//item")[:POST_LIMIT]:

    title = item.find("title").text
    link = item.find("link").text
    desc = item.find("description").text

    desc = clean_text(desc)

    posts.append({
        "title": title,
        "link": link,
        "desc": desc
    })


print(f"📝 {len(posts)}개 글 업데이트")


# ----------------------
# index.html 업데이트
# ----------------------

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- POSTS_START -->"
end = "<!-- POSTS_END -->"

if start not in content or end not in content:
    raise Exception("POSTS_START / POSTS_END 마커가 index.html에 없습니다.")

post_html = "\n<ul>\n"

for p in posts:

    post_html += f"""
<li>
<a href="{p['link']}" target="_blank" rel="noopener noreferrer">
{p['title']}
</a>
<p class="desc">{p['desc']}</p>
</li>
"""

post_html += "\n</ul>\n"

new_content = re.sub(
    f"{start}.*?{end}",
    f"{start}\n{post_html}\n{end}",
    content,
    flags=re.S
)

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ index.html 업데이트 완료")


# ----------------------
# sitemap 생성
# ----------------------

today = datetime.now().strftime("%Y-%m-%d")

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

# 메인 페이지
sitemap += f"""
<url>
<loc>{SITE_URL}</loc>
<lastmod>{today}</lastmod>
<priority>1.0</priority>
</url>
"""

for p in posts:

    sitemap += f"""
<url>
<loc>{p['link']}</loc>
<lastmod>{today}</lastmod>
<priority>0.8</priority>
</url>
"""

sitemap += "</urlset>"

with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write(sitemap)

print("🗺 sitemap.xml 생성 완료")

print("🚀 블로그 업데이트 완료!")

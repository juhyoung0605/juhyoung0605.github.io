import feedparser
import datetime
import os
import re
from urllib.parse import urlparse
from xml.sax.saxutils import escape

# =========================
# 설정
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605.xml"
BASE_URL = "https://juhyoung0605.github.io"
POST_DIR = "posts"

INDEX_FILE = "index.html"
POSTS_FILE = "posts.html"
SITEMAP_FILE = "sitemap.xml"
ROBOTS_FILE = "robots.txt"

MAX_INDEX_POSTS = 5

os.makedirs(POST_DIR, exist_ok=True)

# =========================
# RSS 파싱
# =========================
feed = feedparser.parse(RSS_URL)

posts_meta = []

for entry in feed.entries:
    if not hasattr(entry, "published"):
        continue

    dt = datetime.datetime.strptime(
        entry.published, "%a, %d %b %Y %H:%M:%S %z"
    )
    date_str = dt.strftime("%Y-%m-%d")
    safe_title = re.sub(r"[^\w\-]", "", entry.title.replace(" ", "-")).lower()
    filename = f"{date_str}-{safe_title}.html"
    filepath = os.path.join(POST_DIR, filename)

    summary = re.sub("<[^<]+?>", "", entry.description)
    summary = summary.replace("&nbsp;", " ").strip()

    # posts 개별 html 생성 (이미 있으면 스킵)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{entry.title}</title>
  <meta name="description" content="{summary[:150]}">
  <link rel="canonical" href="{entry.link}">
</head>
<body>
  <h1>{entry.title}</h1>
  <p><a href="{entry.link}" target="_blank">👉 네이버 원문 보기</a></p>
  <p>{summary}</p>
</body>
</html>
""")

    posts_meta.append({
        "title": entry.title,
        "date": date_str,
        "summary": summary[:120] + "...",
        "file": f"{POST_DIR}/{filename}"
    })

# 최신순 정렬
posts_meta.sort(key=lambda x: x["date"], reverse=True)

# =========================
# index.html 생성
# =========================
index_items = ""
for post in posts_meta[:MAX_INDEX_POSTS]:
    index_items += f"""
<li>
  <a href="{post['file']}">{post['title']}</a><br>
  <small>{post['date']} · {post['summary']}</small>
</li>
"""

with open(INDEX_FILE, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>네이버 블로그 아카이브</title>
  <meta name="description" content="네이버 블로그 글을 자동으로 아카이빙한 사이트">
</head>
<body>
  <h1>최근 글</h1>
  <ul>{index_items}</ul>
  <p><a href="posts.html">📚 전체 글 보기</a></p>
</body>
</html>
""")

# =========================
# posts.html 생성
# =========================
posts_items = ""
for post in posts_meta:
    posts_items += f"""
<li>
  <a href="{post['file']}">{post['title']}</a>
  <small>({post['date']})</small>
</li>
"""

with open(POSTS_FILE, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>전체 글 목록</title>
</head>
<body>
  <h1>전체 글</h1>
  <ul>{posts_items}</ul>
  <p><a href="index.html">← 홈으로</a></p>
</body>
</html>
""")

# =========================
# sitemap.xml 생성
# =========================
with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""")

    def add_url(loc):
        f.write(f"""  <url>
    <loc>{escape(loc)}</loc>
  </url>
""")

    add_url(BASE_URL + "/")
    add_url(BASE_URL + "/posts.html")

    for post in posts_meta:
        add_url(f"{BASE_URL}/{post['file']}")

    f.write("</urlset>")

# =========================
# robots.txt 생성
# =========================
with open(ROBOTS_FILE, "w", encoding="utf-8") as f:
    f.write(f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
""")

print("✅ 전체 업데이트 완료")

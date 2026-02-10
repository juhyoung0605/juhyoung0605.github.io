import feedparser
import datetime
import os
import re

# =========================
# 설정
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605"
INDEX_HTML = "index.html"
SITEMAP_XML = "sitemap.xml"
LAST_UPDATE_FILE = "last_update.txt"
UPDATE_INTERVAL_DAYS = 7

TODAY = datetime.date.today()

# =========================
# 마지막 업데이트 날짜 확인
# =========================
if os.path.exists(LAST_UPDATE_FILE):
    with open(LAST_UPDATE_FILE, "r", encoding="utf-8") as f:
        last_date = datetime.date.fromisoformat(f.read().strip())

    if (TODAY - last_date).days < UPDATE_INTERVAL_DAYS:
        print("⏭ 업데이트 스킵: 아직 주 1회 주기 아님")
        exit()

# =========================
# RSS 파싱
# =========================
feed = feedparser.parse(RSS_URL)

# =========================
# index.html용 리스트 생성
# =========================
html_list = ""
for entry in feed.entries[:5]:
    summary = re.sub('<[^<]+?>', '', entry.description)
    summary = summary.replace('&nbsp;', ' ').strip()[:80] + "…"

    html_list += f"""
    <li>
        <a href="{entry.link}" target="_blank" rel="noopener">
            {entry.title}
        </a>
        <p class="desc">{summary}</p>
    </li>
    """

# =========================
# index.html 갱신
# =========================
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- POSTS_START -->"
end = "<!-- POSTS_END -->"

new_content = (
    content[:content.find(start) + len(start)]
    + "\n<ul>\n"
    + html_list
    + "\n</ul>\n"
    + content[content.find(end):]
)

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(new_content)

# =========================
# sitemap.xml (index + 글 링크)
# =========================
with open(SITEMAP_XML, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    f.write(f"""
    <url>
        <loc>https://juhyoung0605.github.io/</loc>
        <lastmod>{TODAY}</lastmod>
    </url>
    """)

    for entry in feed.entries:
        safe_url = entry.link.replace("&", "&amp;")
        f.write(f"""
        <url>
            <loc>{safe_url}</loc>
        </url>
        """)

    f.write("</urlset>")

# =========================
# 마지막 업데이트 날짜 기록
# =========================
with open(LAST_UPDATE_FILE, "w", encoding="utf-8") as f:
    f.write(TODAY.isoformat())

print("✅ 주 1회 업데이트 완료")

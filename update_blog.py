import feedparser
import datetime
import re
from pathlib import Path

# =========================
# 설정
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605"
INDEX_HTML = Path("index.html")
SITEMAP_XML = Path("sitemap.xml")
SITE_URL = "https://juhyoung0605.github.io"

MAX_POSTS = 5

# =========================
# RSS 로드
# =========================
feed = feedparser.parse(RSS_URL)

posts_html = []

for entry in feed.entries[:MAX_POSTS]:
    published = datetime.datetime(*entry.published_parsed[:6])
    date_str = published.strftime("%Y.%m.%d")

    summary = re.sub("<[^>]+>", "", entry.summary)
    summary = summary.replace("&nbsp;", " ").strip()[:100] + "..."

    posts_html.append(
        f"""
        <div class="post-item">
            <a href="{entry.link}" target="_blank"><strong>{entry.title}</strong></a><br>
            <small>📅 {date_str} · {summary}</small>
        </div>
        """
    )

posts_block = "\n".join(posts_html)

# =========================
# index.html 업데이트
# =========================
html = INDEX_HTML.read_text(encoding="utf-8")

start = "<!-- BLOG_UPDATE_START -->"
end = "<!-- BLOG_UPDATE_END -->"

new_html = (
    html[: html.index(start) + len(start)]
    + "\n"
    + posts_block
    + "\n"
    + html[html.index(end) :]
)

INDEX_HTML.write_text(new_html, encoding="utf-8")

# =========================
# sitemap.xml 생성
# =========================
urls = [SITE_URL + "/"]

for entry in feed.entries:
    urls.append(entry.link.split("?")[0])

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for url in urls:
    sitemap.append(f"<url><loc>{url}</loc></url>")

sitemap.append("</urlset>")

SITEMAP_XML.write_text("\n".join(sitemap), encoding="utf-8")

print("✅ index.html & sitemap.xml 업데이트 완료")

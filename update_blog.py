import feedparser
import datetime
import re
import os

# =========================
# 설정 (루트 주소로 변경)
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605"
SITE_URL = "https://juhyoung0605.github.io"
INDEX_HTML = "index.html"
SITEMAP_XML = "sitemap.xml"

# index.html의 마커 이름과 반드시 일치해야 합니다!
START_MARKER = ""
END_MARKER = ""

# =========================
# RSS 파싱
# =========================
feed = feedparser.parse(RSS_URL)

# 최근 게시물 HTML 생성
recent_html = ""
for entry in feed.entries[:5]:
    dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    date_str = dt.strftime("%Y.%m.%d")
    summary = re.sub("<[^<]+?>", "", entry.description).replace("&nbsp;", " ").strip()[:120] + "..."
    
    recent_html += f"""
    <div class="recent-item" style="margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;">
        <a href="{entry.link}" target="_blank" rel="noopener noreferrer" style="font-weight:bold; color:#0056b3; text-decoration:none;">
            {entry.title}
        </a>
        <p style="margin:5px 0; font-size:0.85em; color:#666;">
            📅 {date_str} | {summary}
        </p>
    </div>\n"""

# =========================
# index.html 업데이트
# =========================
if os.path.exists(INDEX_HTML):
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER in content and END_MARKER in content:
        parts = content.split(START_MARKER)
        header = parts[0]
        footer = parts[1].split(END_MARKER)[1]
        
        new_content = header + START_MARKER + "\n" + recent_html + END_MARKER + footer

        with open(INDEX_HTML, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ index.html 업데이트 완료")
    else:
        print("❌ 에러: 마커를 찾을 수 없습니다. index.html의 주석을 확인하세요.")
        exit(1)

# =========================
# sitemap.xml & robots.txt 생성
# =========================
with open(SITEMAP_XML, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write(f"  <url><loc>{SITE_URL}/</loc><priority>1.0</priority></url>\n")
    for entry in feed.entries:
        safe_link = entry.link.replace("&", "&amp;")
        f.write(f"  <url><loc>{safe_link}</loc><priority>0.8</priority></url>\n")
    f.write('</urlset>')

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml")
print("✅ 사이트맵 및 robots.txt 생성 완료")

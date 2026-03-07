import feedparser
import datetime
import os
import re

# =========================
# 설정 (루트 주소 기준)
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605"
SITE_URL = "https://juhyoung0605.github.io"
INDEX_HTML = "index.html"
SITEMAP_XML = "sitemap.xml"
LAST_UPDATE_FILE = "last_update.txt"
UPDATE_INTERVAL_DAYS = 0  # 테스트를 위해 우선 0으로 설정 (매번 업데이트)

TODAY = datetime.date.today()

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
    </li>\n"""

# =========================
# index.html 갱신
# =========================
with open(INDEX_HTML, "r", encoding="utf-8") as f:
    content = f.read()

# 주형님의 HTML 마커 이름과 일치시키세요 (POSTS_START 인지 START_POSTS 인지 확인!)
start = "<!-- POSTS_START -->"
end = "<!-- POSTS_END -->"

# 마커 존재 여부 확인
if start not in content or end not in content:
    raise Exception("POSTS_START / POSTS_END 마커가 index.html에 없습니다.")

new_content = (
    content.split(start)[0]
    + start
    + "\n<ul>\n"
    + html_list
    + "</ul>\n"
    + end
    + content.split(end)[1]
)

with open(INDEX_HTML, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ index.html 업데이트 완료")

# =========================
# sitemap.xml 생성 (RSS + 주요 게시물 수동 추가)
# =========================
# 주형님이 꼭 넣고 싶은 글 리스트
IMPORTANT_POSTS = [
    "https://blog.naver.com/jubro_0605/224091794208",
    "https://blog.naver.com/jubro_0605/224113377005",
    "https://blog.naver.com/jubro_0605/224134992517",
    "https://blog.naver.com/jubro_0605/224156241781",
    "https://blog.naver.com/jubro_0605/224168890646",
    "https://blog.naver.com/jubro_0605/224128044251"
]

with open(SITEMAP_XML, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    # 1. 메인 주소 (juhyoung0605.github.io)
    f.write(f"  <url><loc>{SITE_URL}/</loc><lastmod>{TODAY}</lastmod><priority>1.0</priority></url>\n")

    # 2. RSS를 통한 최신 글 (자동 추출)
    rss_links = []
    for entry in feed.entries:
        safe_url = entry.link.replace("&", "&amp;")
        rss_links.append(entry.link) # 중복 체크용 원본 링크 저장
        f.write(f"  <url><loc>{safe_url}</loc><priority>0.8</priority></url>\n")

    # 3. 주형님이 지정한 중요 게시물 (RSS에 없을 경우 대비)
    for post_url in IMPORTANT_POSTS:
        # RSS에 이미 포함된 글은 중복으로 넣지 않음
        if post_url not in rss_links:
            safe_url = post_url.replace("&", "&amp;")
            f.write(f"  <url><loc>{safe_url}</loc><priority>0.9</priority></url>\n")

    f.write("</urlset>")

print(f"✅ sitemap.xml 생성 완료 (주요 게시물 {len(IMPORTANT_POSTS)}개 포함)")

# =========================
# robots.txt 생성
# =========================
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml")
print("✅ robots.txt 생성 완료")

# 마지막 업데이트 날짜 기록
with open(LAST_UPDATE_FILE, "w", encoding="utf-8") as f:
    f.write(TODAY.isoformat())

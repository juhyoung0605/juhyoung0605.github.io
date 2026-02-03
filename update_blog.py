import feedparser
import datetime
import re
import os

# =========================
# 설정
# =========================
RSS_URL = "https://rss.blog.naver.com/jubro_0605"
SITE_URL = "https://juhyoung0605.github.io"
INDEX_HTML = "index.html"
SITEMAP_XML = "sitemap.xml"

START_MARKER = "<!-- START_RECENT_POSTS -->"
END_MARKER = "<!-- END_RECENT_POSTS -->"

# =========================
# RSS 파싱
# =========================
feed = feedparser.parse(RSS_URL)

# =========================
# Recent Updates HTML 생성
# =========================
recent_html = ""

for entry in feed.entries[:5]:
    dt = datetime.datetime.strptime(
        entry.published, "%a, %d %b %Y %H:%M:%S %z"
    )
    date_str = dt.strftime("%Y.%m.%d")

    summary = re.sub("<[^<]+?>", "", entry.description)
    summary = summary.replace("&nbsp;", " ").strip()[:120] + "..."

    recent_html += f"""
    <div class="recent-item">
        <a href="{entry.link}" target="_blank" rel="noopener noreferrer">
            {entry.title}
        </a>
        <p style="margin:5px 0; font-size:0.85em; color:#666;">
            📅 {date_str} | {summary}
        </p>
    </div>
    """

# =========================
# index.html 업데이트
# =========================
if os.path.exists(INDEX_HTML):
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER in content and END_MARKER in content:
        new_content = (
            content.split(START_MARKER)[0]
            + START_MARKER
            + recent_html
            + END_MARKER
            + content.split(END_MARKER)[1]
        )

        with open(INDEX_HTML, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("✅ index.html Recent Updates 업데이트 완료")

# =========================
# sitemap.xml 생성 (GitHub Pages 전용)
# =========================
with open(SITEMAP_XML, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    # index
    f.write("  <url>\n")
    f.write(f"    <loc>{SITE_URL}/</loc>\n")
    f.write("    <changefreq>daily</changefreq>\n")
    f.write("    <priority>1.0</priority>\n")
    f.write("  </url>\n")

    # posts (GitHub Pages 기준 URL만 포함)
    for entry in feed.entries:
        match = re.search(r"/(\d+)", entry.link)
        if not match:
            continue

        post_id = match.group(1)

        dt = datetime.datetime.strptime(
            entry.published, "%a, %d %b %Y %H:%M:%S %z"
        )
        lastmod = dt.strftime("%Y-%m-%d")

        f.write("  <url>\n")
        f.write(f"    <loc>{SITE_URL}/posts/{post_id}.html</loc>\n")
        f.write(f"    <lastmod>{lastmod}</lastmod>\n")
        f.write("    <changefreq>monthly</changefreq>\n")
        f.write("    <priority>0.8</priority>\n")
        f.write("  </url>\n")

    f.write("</urlset>")

print("✅ sitemap.xml 생성 완료")


# =========================
# posts/*.html 자동 생성
# =========================
POST_DIR = "posts"
os.makedirs(POST_DIR, exist_ok=True)

POST_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>{title} | Jublog Archive</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{naver_url}">
</head>
<body>

<h1>{title}</h1>
<p><strong>게시일:</strong> {date}</p>

<section>
  <h2>요약</h2>
  <p>{summary}</p>
</section>

<section>
  <p>
    👉 전체 내용은
    <a href="{naver_url}" target="_blank" rel="noopener noreferrer">
      네이버 블로그
    </a>
    에서 확인할 수 있습니다.
  </p>
</section>

</body>
</html>
"""

for entry in feed.entries:
    match = re.search(r"/(\d+)", entry.link)
    if not match:
        continue

    post_id = match.group(1)
    post_path = os.path.join(POST_DIR, f"{post_id}.html")

    # 이미 있으면 재생성하지 않음 (불필요한 커밋 방지)
    if os.path.exists(post_path):
        continue

    dt = datetime.datetime.strptime(
        entry.published, "%a, %d %b %Y %H:%M:%S %z"
    )
    date_str = dt.strftime("%Y.%m.%d")

    raw_summary = re.sub("<[^<]+?>", "", entry.description)
    raw_summary = raw_summary.replace("&nbsp;", " ").strip()

    summary = raw_summary[:500]
    if not summary.endswith("."):
        summary += "."

    html = POST_TEMPLATE.format(
        title=entry.title,
        description=entry.title,
        date=date_str,
        summary=summary,
        naver_url=entry.link
    )

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(html)

print("✅ posts/*.html 자동 생성 완료")


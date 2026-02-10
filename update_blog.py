import feedparser
import datetime
import re

RSS_URL = "https://rss.blog.naver.com/jubro_0605"
INDEX_FILE = "index.html"
SITEMAP_FILE = "sitemap.xml"
SITE_URL = "https://juhyoung0605.github.io"

def clean_html(text):
    return re.sub("<[^<]+?>", "", text).replace("&nbsp;", " ").strip()

def main():
    feed = feedparser.parse(RSS_URL)

    # 1. 최신 글 리스트 생성
    post_html = ""
    for entry in feed.entries[:10]:
        date = datetime.datetime.strptime(
            entry.published, "%a, %d %b %Y %H:%M:%S %z"
        ).strftime("%Y.%m.%d")

        summary = clean_html(entry.description)[:100] + "..."

        post_html += f"""
        <div class="post-item">
            <a href="{entry.link}" target="_blank">{entry.title}</a>
            <p class="post-meta">{date} · {summary}</p>
        </div>
        """

    # 2. index.html 업데이트
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    html = re.sub(
        r"<!-- POSTS_START -->.*?<!-- POSTS_END -->",
        f"<!-- POSTS_START -->{post_html}<!-- POSTS_END -->",
        html,
        flags=re.S,
    )

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    # 3. sitemap.xml 생성
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f"<url><loc>{SITE_URL}</loc></url>\n")

        for entry in feed.entries:
            f.write(f"<url><loc>{entry.link}</loc></url>\n")

        f.write("</urlset>")

    print("✅ index.html & sitemap.xml 업데이트 완료")

if __name__ == "__main__":
    main()

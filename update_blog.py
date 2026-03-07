import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape

RSS_URL = "https://rss.blog.naver.com/jubro_0605.xml"
INDEX_FILE = "index.html"
SITEMAP_FILE = "sitemap.xml"

MAX_POSTS = 10


def fetch_rss():
    response = requests.get(RSS_URL)
    response.raise_for_status()
    return response.text


def parse_rss(xml_data):
    root = ET.fromstring(xml_data)

    items = []
    for item in root.findall(".//item")[:MAX_POSTS]:

        title = item.findtext("title", "")
        link = item.findtext("link", "")
        desc = item.findtext("description", "")
        pub_date = item.findtext("pubDate", "")

        # description 정리
        desc = desc.replace("<![CDATA[", "").replace("]]>", "")
        desc = desc[:120]

        items.append({
            "title": title,
            "link": link,
            "desc": desc,
            "date": pub_date
        })

    return items


def generate_post_html(posts):

    html = "<ul>\n"

    for post in posts:

        title = escape(post["title"])
        link = escape(post["link"])
        desc = escape(post["desc"])

        html += f"""
    <li>
        <a href="{link}" target="_blank" rel="noopener">
            {title}
        </a>
        <p class="desc">{desc}</p>
    </li>
"""

    html += "\n</ul>"

    return html


def update_index(posts):

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- POSTS_START -->"
    end = "<!-- POSTS_END -->"

    if start not in content or end not in content:
        raise Exception("POSTS_START / POSTS_END 마커가 index.html에 없습니다.")

    new_posts = generate_post_html(posts)

    updated = content.split(start)[0] + start + "\n" + new_posts + "\n" + end + content.split(end)[1]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(updated)


def generate_sitemap(posts):

    today = datetime.utcnow().strftime("%Y-%m-%d")

    urls = f"""
<url>
    <loc>https://juhyoung0605.github.io/</loc>
    <lastmod>{today}</lastmod>
</url>
"""

    for post in posts:

        link = escape(post["link"])

        urls += f"""
<url>
    <loc>{link}</loc>
    <lastmod>{today}</lastmod>
</url>
"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap)


def main():

    print("RSS 가져오는 중...")
    xml_data = fetch_rss()

    print("RSS 파싱 중...")
    posts = parse_rss(xml_data)

    print("index.html 업데이트...")
    update_index(posts)

    print("sitemap.xml 생성...")
    generate_sitemap(posts)

    print("완료!")


if __name__ == "__main__":
    main()

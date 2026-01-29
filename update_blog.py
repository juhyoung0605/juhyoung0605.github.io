import feedparser
import datetime
import re
import os

# 1. 설정
rss_url = "https://rss.blog.naver.com/jubro_0605"
html_path = "index.html"
sitemap_path = "sitemap.xml"

# 2. RSS 피드 가져오기
feed = feedparser.parse(rss_url)

# 3. HTML 최근 게시물 리스트 생성
html_list = ""
for entry in feed.entries[:5]:
    dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    date_str = dt.strftime("%Y.%m.%d")
    summary = re.sub('<[^<]+?>', '', entry.description).replace('&nbsp;', ' ').strip()[:100] + "..."
    
    html_list += f"<div style='margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;'>"
    html_list += f"<a href='{entry.link}' target='_blank' style='font-weight:bold; color:#0056b3; text-decoration:none;'>{entry.title}</a>"
    html_list += f"<p style='margin:5px 0; font-size:0.85em; color:#666;'>📅 {date_str} | {summary}</p></div>\n"

# 4. sitemap.xml 생성 (& 문자를 &amp;로 변환하여 에러 방지)
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write('  <url><loc>https://juhyoung0605.github.io/</loc></url>\n')
    for entry in feed.entries:
        # URL 내의 & 기호를 XML 표준인 &amp;로 치환합니다 (핵심 수정 사항)
        safe_link = entry.link.replace("&", "&amp;")
        f.write(f'  <url><loc>{safe_link}</loc></url>\n')
    f.write('</urlset>')

# 5. index.html 업데이트
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker, end_marker = "", ""
    if start_marker in content and end_marker in content:
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)
        
        new_content = content[:start_index] + "\n" + html_list + content[end_index:]
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ 업데이트 완료 (사이트맵 특수문자 처리 포함)")

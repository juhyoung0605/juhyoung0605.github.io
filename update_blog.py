import feedparser
import datetime
import re
import os

# 1. 설정
rss_url = "https://rss.blog.naver.com/jubro_0605"
readme_path = "index.md"
sitemap_path = "sitemap.xml"
meta_tag = '<meta name="google-site-verification" content="qgTCNSJjyI0DQd79vN5CcpnfcIZ6QgkVvtnLzvkPQFw" />'

# 2. RSS 피드 가져오기
feed = feedparser.parse(rss_url)

# 3. 마크다운 및 사이트맵 데이터 생성
markdown_text = ""
for entry in feed.entries[:5]: # index.md에는 최신 5개만
    dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    date_str = dt.strftime("%Y.%m.%d")
    summary = re.sub('<[^<]+?>', '', entry.description).replace('&nbsp;', ' ').strip()
    if len(summary) > 100: summary = summary[:100] + "..."
    
    markdown_text += f"### 📄 [{entry.title}]({entry.link})\n"
    markdown_text += f"> 📅 {date_str} <br>\n"
    markdown_text += f"> {summary}\n\n"

# 4. sitemap.xml 생성 (모든 글 포함)
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    f.write('  <url><loc>https://juhyoung0605.github.io/</loc></url>\n')
    for entry in feed.entries:
        f.write(f'  <url><loc>{entry.link}</loc></url>\n')
    f.write('</urlset>')

# 5. index.md 업데이트
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker = ""
    end_marker = ""
    
    if start_marker in content and end_marker in content:
        # 메타 태그 체크 및 최상단 유지
        if meta_tag not in content:
            content = meta_tag + "\n\n" + content
        
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)
        new_content = content[:start_index] + "\n" + markdown_text + content[end_index:]
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ 업데이트 성공")
    else:
        print("❌ 마커를 찾을 수 없습니다.")

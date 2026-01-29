import feedparser
import datetime
import re

# 1. 설정 및 경로
rss_url = "https://rss.blog.naver.com/jubro_0605"
readme_path = "index.md"
sitemap_path = "sitemap.xml"
# 구글 서치 콘솔 인증 태그
meta_tag = '<meta name="google-site-verification" content="qgTCNSJjyI0DQd79vN5CcpnfcIZ6QgkVvtnLzvkPQFw" />\n\n'

# 2. RSS 피드 가져오기
feed = feedparser.parse(rss_url)

# 3. 마크다운 텍스트 및 사이트맵 데이터 생성
markdown_text = ""
blog_urls = []

for entry in feed.entries[:5]: # 최신글 5개
    dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    date_str = dt.strftime("%Y.%m.%d")
    
    summary = re.sub('<[^<]+?>', '', entry.description)
    if len(summary) > 100:
        summary = summary[:100] + "..."
    
    markdown_text += f"### 📄 [{entry.title}]({entry.link})\n"
    markdown_text += f"> 📅 {date_str} <br>\n"
    markdown_text += f"> {summary}\n\n"
    blog_urls.append(entry.link)

# 4. sitemap.xml 자동 생성 로직
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    # 기본 도메인 추가
    f.write('  <url><loc>https://juhyoung0605.github.io/</loc></url>\n')
    # RSS 내 모든 포스팅 추가
    for entry in feed.entries:
        f.write(f'  <url><loc>{entry.link}</loc></url>\n')
    f.write('</urlset>')

# 5. index.md 업데이트 (메타 태그 유지 및 마커 교체)
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 마커 설정 (기존 파일에 아래 주석이 있어야 함)
start_marker = ""
end_marker = ""

if start_marker in content and end_marker in content:
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker)
    
    # 1. 메타 태그가 없으면 최상단에 추가
    if "google-site-verification" not in content:
        content = meta_tag + content
        # 위치 재계산
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)

    new_content = content[:start_index] + "\n" + markdown_text + content[end_index:]
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("성공: index.md 및 sitemap.xml 업데이트 완료")
else:
    # 마커가 없을 경우 새로 생성 (보안책)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(meta_tag)
        f.write("# 주블로그 최근 포스팅\n\n")
        f.write(start_marker + "\n" + markdown_text + "\n" + end_marker)
    print("주의: 마커가 없어 파일을 새로 구성했습니다.")

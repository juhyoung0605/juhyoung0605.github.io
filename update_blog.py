import feedparser
import datetime
import re
import os

# 1. 설정 및 경로
rss_url = "https://rss.blog.naver.com/jubro_0605"
readme_path = "index.md"
sitemap_path = "sitemap.xml"
# 구글 서치 콘솔 인증 태그 (절대 삭제되지 않도록 상단 고정용)
meta_tag = '<meta name="google-site-verification" content="qgTCNSJjyI0DQd79vN5CcpnfcIZ6QgkVvtnLzvkPQFw" />'

# 2. RSS 피드 가져오기
feed = feedparser.parse(rss_url)

# 3. 마크다운 텍스트 및 사이트맵 데이터 생성
markdown_text = ""
for entry in feed.entries[:5]: # 최신글 5개만 index.md에 노출
    # 날짜 처리
    try:
        dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
        date_str = dt.strftime("%Y.%m.%d")
    except:
        date_str = datetime.datetime.now().strftime("%Y.%m.%d")
    
    # 요약글 처리 (HTML 제거 및 말줄임)
    summary = re.sub('<[^<]+?>', '', entry.description)
    summary = summary.replace('&nbsp;', ' ').strip()
    if len(summary) > 100:
        summary = summary[:100] + "..."
    
    markdown_text += f"### 📄 [{entry.title}]({entry.link})\n"
    markdown_text += f"> 📅 {date_str} <br>\n"
    markdown_text += f"> {summary}\n\n"

# 4. sitemap.xml 자동 생성 로직 (RSS 내 모든 글 포함)
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    # 깃허브 페이지 본체 주소
    f.write('  <url><loc>https://juhyoung0605.github.io/</loc></url>\n')
    # 네이버 블로그의 모든 포스팅을 구글이 긁어가도록 추가
    for entry in feed.entries:
        f.write(f'  <url><loc>{entry.link}</loc></url>\n')
    f.write('</urlset>')

# 5. index.md 업데이트 로직
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
else:
    content = ""

# 마커 설정 (주형님의 index.md에 있는 태그 기준)
start_marker = ""
end_marker = ""

# 메타 태그가 파일에 없으면 최상단에 추가
if meta_tag not in content:
    content = meta_tag + "\n\n" + content

if start_marker in content and end_marker in content:
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker)
    
    # 마커 사이의 내용만 교체
    new_content = content[:start_index] + "\n" + markdown_text + content[end_index:]
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ 성공: index.md 마커 영역 및 sitemap.xml 업데이트 완료")
else:
    # 마커를 찾을 수 없을 때의 안전장치 (파일 재구성)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(meta_tag + "\n\n")
        f.write("# Recent Updates\n")
        f.write(start_marker + "\n" + markdown_text + end_marker + "\n\n")
        f.write(content.replace(meta_tag, "").strip())
    print("⚠️ 주의: 마커를 찾지 못해 파일을 재구성했습니다. 위치를 확인하세요.")

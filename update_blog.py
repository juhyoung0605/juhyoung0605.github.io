import feedparser
import datetime
import re # HTML 태그 제거용

# 1. 네이버 블로그 RSS 주소
rss_url = "https://rss.blog.naver.com/jubro_0605"

# 2. RSS 피드 가져오기
feed = feedparser.parse(rss_url)

# 3. 마크다운 형식으로 변환 (최신글 5개만)
markdown_text = ""
for entry in feed.entries[:5]:
    # 날짜 포맷 (YYYY.MM.DD)
    dt = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    date_str = dt.strftime("%Y.%m.%d")
    
    # 요약글(Description) 가져오기 및 태그 제거
    summary = entry.description
    summary = re.sub('<[^<]+?>', '', summary) # HTML 태그 제거
    if len(summary) > 100: # 너무 길면 100자에서 자르기
        summary = summary[:100] + "..."
    
    # 마크다운 작성 (제목 + 날짜 + 요약)
    markdown_text += f"### 📄 [{entry.title}]({entry.link})\n"
    markdown_text += f"> 📅 {date_str} <br>\n"
    markdown_text += f"> {summary}\n\n"

# 4. index.md 파일 읽기
readme_path = "index.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 5. 마커 사이의 내용 교체하기
start_marker = ""
end_marker = ""

if start_marker in content and end_marker in content:
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker)
    
    # 기존 내용 앞 + 새 내용 + 기존 내용 뒤
    new_content = content[:start_index] + "\n" + markdown_text + content[end_index:]
    
    # 파일 저장
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("업데이트 완료! (요약 포함)")
else:
    print("마커를 찾을 수 없습니다. index.md에 와 를 추가하세요.")

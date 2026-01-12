import json
from collections import defaultdict

# 1. JSON 파일 읽기
with open('entitle_bible_context.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

book_names = {
	book_code: book_info['korean_name']
	for book_code, book_info in bible_info.items()
}

# 2. 권별, 장별로 구절 그룹화
books = defaultdict(lambda: defaultdict(list))

for verse in data['verses']:
	parts = verse['id'].split('.')
	book_code = parts[0]      # GEN
	chapter = parts[1]         # 1
	verse_num = parts[2]       # 1
	
	books[book_code][chapter].append({
		'num': verse_num,
		'text': verse['text']
	})

for book_code, chapters in books.items():
	book_name = book_names[book_code]
	
	# xHTML 시작
	html = '<?xml version="1.0" encoding="utf-8"?>\n'
	html += f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
	<meta charset="UTF-8"/>
	<title>{book_name}</title>
	<link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
'''
	
	# 각 장 추가 (숫자 순서대로)
	for chapter_num in sorted(chapters.keys(), key=int):
		chapter_num = int(chapter_num)

		def get_chapter_id(book_code, chapter_num) :
			return f"ch_{book_code}_{chapter_num}"

		def get_next_chapter_id(book_code, chapter_num) :
			# 요한계시록 22장일 경우
			if book_code == "REV" and chapter_num == 22 : return "ch_REV_22"
			# 마지막 장일 경우
			if bible_info[book_code]["chapter_num"] == chapter_num :
				for key, value in bible_info.items():
					if value.get("order") == int(bible_info[book_code]["order"])+1:
						return f"ch_{key}_1"
			# 일반적인 경우
			return f"ch_{book_code}_{chapter_num+1}"
		

		def get_next_chapter_page(book_code, chapter_num) :
			if book_code == "REV" and chapter_num == 22 : return "66_REV.xhtml"
			
			if bible_info[book_code]["chapter_num"] == chapter_num :
				for key, value in bible_info.items():
					if value.get("order") == int(bible_info[book_code]["order"])+1:
						return f'{'%02d'%int(bible_info[book_code]["order"]+1)}_{key}.xhtml'
			else : return ''

		html += f'''<div class="chapter" id="{get_chapter_id(book_code, chapter_num)}">
	<div class="header">
		<div class="headerIndexBox">
			<a class="oldTestamentIndex">구약전서</a>
			<a class="newTestamentIndex">신약전서</a>
		</div> <!-- headerIndexBox -->
		<h2>{book_name}</h2>
		<h1><a href="{get_next_chapter_page(book_code, chapter_num)}#{get_next_chapter_id(book_code, chapter_num)}">{chapter_num}장</a></h1>
	</div> <!-- header -->
	<div class="section">
'''
		
		for verse in chapters[str(chapter_num)]:
			verse["text"] = verse["text"].replace('\n', '<br/>')
			html += f'		<div class="verse"><p class="verseNum">{verse["num"]}</sup><p class="verseText">{verse["text"]}</p></div>\n'

		html += f'''</div> <!-- section -->
	<div class="footer">
		<a class="entitleIndex">┼</a>
		<a class="chapterIndex">{book_name[0]}</a>
		<a class="home" href="#{get_chapter_id(book_code, chapter_num)}">{chapter_num}</a>
	</div> <!-- footer -->
	<div class="pagebreak"></div>
</div> <!-- chapter -->
'''
	
	# 파일 저장
	html += '\n</body>\n</html>'
	filename = f'pages/{'%02d'%int(bible_info[book_code]["order"])}_{book_code}.xhtml'
	with open(filename, 'w', encoding='utf-8') as f:
			f.write(html)
	
	print(f'생성됨: {filename} ({book_name})')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
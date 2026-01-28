import json

from getter import *

# 1. JSON 파일 읽기
with open('entitle_bible_context.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

for book_code in bible_info:
	testament_type = ''
	if bible_info[book_code]['is_old_testament'] :
		testament_type = 'oldTestament'
	else :
		testament_type = 'newTestament'
		
	html = '<?xml version="1.0" encoding="utf-8"?>\n'
	html += f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
	
	<title>chapter_index_{book_code}</title>
	<link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="chapterIndex">
	<div class="chapterIndex_{testament_type}Header">
		<div class="chapterIndex_{testament_type}KoreanBookName">{bible_info[book_code]["korean_name"]}</div>
		<div class="chapterIndex_{testament_type}EnglishBookName">({bible_info[book_code]["full_name"]})</div>
	</div> <!-- chapterIndex_{testament_type}Header -->
	<div class="chapterIndex_section">'''

	# 전 버튼
	html += f'		<div class="{testament_type}IndexBtn" id="chapter_index_{book_code}_0"><a href="{get_page_index_xhtml_name()}">성경</a></div>\n'
	
	# 챕터 버튼들
	for i in range(bible_info[book_code]["chapter_num"]):
		chapter_num = i + 1
		html += f'''		<div class="{testament_type}IndexBtn" id="chapter_index_{book_code}_{chapter_num}">
			<a href="{get_page_body_xhtml_name(book_code)}#{get_chapter_id(book_code, chapter_num)}">
				{chapter_num}
			</a>
		</div> <!-- {testament_type}IndexBtn -->'''

	html += f'''\t</div> <!-- chapterIndex_section -->
</div> <!-- chapterIndex -->
</body>
</html>'''

	# 파일 저장
	filename = f'pages/chapter_index/{get_page_chapter_index_xhtml_name(book_code)}'
	with open(filename, 'w', encoding='utf-8') as f:
			f.write(html)
			print(f'생성됨: {filename} ({book_code})')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
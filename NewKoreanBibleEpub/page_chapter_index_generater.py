import json

from getter import get_chapter_id, get_page_body_xhtml_name, get_page_chapter_index_xhtml_name

# 1. JSON 파일 읽기
with open('entitle_bible_context.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

for book_code in bible_info:
	html = '<?xml version="1.0" encoding="utf-8"?>\n'
	html += f'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
	<meta charset="UTF-8"/>
	<title>chapter_index_{book_code}</title>
	<link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="chapterIndex">
	<div class="chapterIndex_header">
		<h1>{bible_info[book_code]["korean_name"]}</h1>
		<h2>({bible_info[book_code]["full_name"]})</h2>
	</div> <!-- chapterIndex_header -->
	<div class="chapterIndex_section">
'''

	html += f'''
		<div class="chapterIndex_chapterBtn" id="chapter_index_{book_code}_0"><a>전</a></div>
'''
	for i in range(bible_info[book_code]["chapter_num"]) :
		chapter_num = i+1
		html += f'''
		<div class="chapterIndex_chapterBtn" id="chapter_index_{book_code}_{chapter_num}">
			<a href="{get_page_body_xhtml_name(book_code)}#{get_chapter_id(book_code, chapter_num)}">
				{chapter_num}
			</a>
		</div> <!-- chapterIndex_chapterBtn -->
'''

	html += f'''
	</div> <!-- chapterIndex_section -->
</div> <!-- chapterIndex -->
</body>
'''

	# 파일 저장
	html += '\n</body>\n</html>'
	filename = f'pages/chapter_index/{get_page_chapter_index_xhtml_name(book_code)}'
	with open(filename, 'w', encoding='utf-8') as f:
			f.write(html)
			print(f'생성됨: {filename} ({book_code})')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
import json

from getter import *
from page_body_generater import book_names

with open('entitle_bible_context.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

html = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
	<meta charset="UTF-8"/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
	<title>index</title>
	<link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="index">
	<div class="index_header">
		<div class="index_headerText">새한글성경</div>
	</div> <!-- index_header -->
	<div class="index_section">
'''

for book_code in book_names :
	testament_type = ''
	if bible_info[book_code]['is_old_testament'] :
		testament_type = 'oldTestament'
	else :
		testament_type = 'newTestament'

	html += f'		<div class="{testament_type}IndexBtn" id="index_{book_code}"><a href="{get_page_chapter_index_xhtml_name(book_code)}">{bible_info[book_code]['korean_concise_name']}</a></div>\n'


html += f'		<div class="GOSIndexBtn" id="index_GOS"><a href="{get_page_GOS_body_xhtml_name()}">복음</a></div>\n'

html += '''
	</div> <!-- index_section -->
</div> <!-- index -->
</body>
</html>
'''

filename = f'pages/{get_index_xhtml_name()}'
with open(filename, 'w', encoding='utf-8') as f:
	f.write(html)
	print(f'생성됨: {filename}')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
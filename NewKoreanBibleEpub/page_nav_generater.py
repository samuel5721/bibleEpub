import json

from getter import get_page_chapter_index_xhtml_name

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

with open('bible_series.json', 'r', encoding='utf-8') as f:
  bible_series = json.load(f)

html = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head>
  <title>nav 새한글</title>
  <meta charset="utf-8"/>
  <link href="../Styles/sgc-nav.css" rel="stylesheet" type="text/css"/>
</head>
<body epub:type="frontmatter">
  <nav epub:type="toc" id="toc" role="doc-toc">
    <h1>차례</h1>
    <ol>
      <li><a href="{get_page_chapter_index_xhtml_name(bible_series[0])}">구약전서</a>
        <ol>
'''

for testament in bible_series:
  if testament == "MAT" :
    html += f'''
        </ol>
      </li>
      <li><a href="{get_page_chapter_index_xhtml_name("MAT")}">신약전서</a>
        <ol>
'''
  html += f'         <li><a href="{get_page_chapter_index_xhtml_name(testament)}">{bible_info[testament]["korean_name"]}</a></li>\n'

html += f'''
        </ol>
      </li>
    </ol>
  </nav>
</body>
</html>
'''

	# 파일 저장
filename = f'pages/nav.xhtml'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'생성됨: {filename}')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
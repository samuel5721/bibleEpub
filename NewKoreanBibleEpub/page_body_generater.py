import json
from collections import defaultdict

from getter import *

def parse_char_pos(footnote_location) :
	# footnote location: BOOK.CHAPTER.VERSE.CHARCOUNT
	try :
		return int(footnote_location.split('.')[3])
	except Exception as e :
		print(f"*** error: invalid footnote id {footnote_location} ({e})")
		return 0

def insert_footnote_marks(verse_text, verse_id, verse_footnotes, start_index, collected) :
	# verse_footnotes: same verse only
	sorted_fn = sorted(verse_footnotes, key=lambda fn: parse_char_pos(fn['location']))
	offset = 0
	index = start_index
	for fn in sorted_fn :
		pos = parse_char_pos(fn['location'])
		mark = f'<a epub:type="noteref" class="footnoteMark" id="{get_start_footnote_id(fn["id"])}" href="#{get_end_footnote_id(fn["id"])}">{index})</a>'
		insert_at = pos + offset
		verse_text = verse_text[:insert_at] + mark + verse_text[insert_at:]
		offset += len(mark)
		collected.append((index, fn))
		index += 1
	return verse_text, index

def get_next_chapter_id(book_code, chapter_num) :
			# 요한계시록 22장일 경우 복음으로 이동
			if book_code == "REV" and chapter_num == 22 : return get_GOS_id()
			# 마지막 장일 경우
			if bible_info[book_code]["chapter_num"] == chapter_num :
				for key, value in bible_info.items():
					if value.get("order") == int(bible_info[book_code]["order"])+1:
						return get_chapter_id(key, 1)
			# 일반적인 경우
			return get_chapter_id(book_code, chapter_num+1)
		

def get_next_chapter_page(book_code, chapter_num) :
	# 요한계시록 22장일 경우
	if book_code == "REV" and chapter_num == 22 : return get_page_GOS_body_xhtml_name()
	
	if bible_info[book_code]["chapter_num"] == chapter_num :
		for key, value in bible_info.items():
			if value.get("order") == int(bible_info[book_code]["order"])+1:
				return get_page_body_xhtml_name(key)
	else : return ''


def get_prev_chapter_id(book_code, chapter_num) :
	# 1장일 경우: 이전 권의 마지막 장. 첫 권(GEN) 1장이면 자기 자신
	if chapter_num == 1 :
		prev_order = int(bible_info[book_code]["order"]) - 1
		if prev_order < 1 :
			return get_chapter_id(book_code, 1)
		for key, value in bible_info.items() :
			if value.get("order") == prev_order :
				return get_chapter_id(key, int(value["chapter_num"]))
		return get_chapter_id(book_code, chapter_num)
	return get_chapter_id(book_code, chapter_num - 1)


def get_prev_chapter_page(book_code, chapter_num) :
	# 1장일 경우: 이전 권의 마지막 장 페이지. 첫 권(GEN) 1장이면 자기 자신(같은 페이지)
	if chapter_num == 1 :
		prev_order = int(bible_info[book_code]["order"]) - 1
		if prev_order < 1 :
			return ''
		for key, value in bible_info.items() :
			if value.get("order") == prev_order :
				return get_page_body_xhtml_name(key)
		return ''
	return ''

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
	parts = verse['location'].split('.')
	book_code = parts[0]      # GEN
	chapter = parts[1]         # 1
	verse_num = parts[2]       # 1
	
	books[book_code][chapter].append({
		'num': verse_num,
		'location': verse['location'],
		'id': verse['id'],
		'text': verse['text']
	})

for book_code, chapters in books.items():
	book_name = bible_info[book_code]["korean_name"]
	
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

		# 해당 장의 모든 주석 미리 수집
		chapter_footnotes = [
			fn for fn in data['footnotes']
			if get_book_code(fn['location']) == book_code and int(get_chapter_num(fn['location'])) == chapter_num
		]
		footnoteIndex = 1
		collected_footnotes = []

		is_paragraph_open = False

		html += f'''<div class="chapter" id="{get_chapter_id(book_code, chapter_num)}">
	<div class="header">
		<p class="bookName"><a href="{get_page_index_xhtml_name()}">{book_name}</a></p>
		<div class="chapterNumBox">
			<div class="chapterMoveBtn"><a href="{get_prev_chapter_page(book_code, chapter_num)}#{get_prev_chapter_id(book_code, chapter_num)}">◀</a></div>
			<p class="chapterNum"><a href="{get_page_chapter_index_xhtml_name(book_code)}">{chapter_num}장</a></p>
			<div class="chapterMoveBtn"><a href="{get_next_chapter_page(book_code, chapter_num)}#{get_next_chapter_id(book_code, chapter_num)}">▶</a></div>
		</div> <!-- chapterNumBox -->
	</div> <!-- header -->
	<div class="section">
		<div class="content">
'''
		for verse in chapters[str(chapter_num)]:

			for paragraph in data['paragraphs'] :
				if paragraph.get("location") == verse['location'] :
					if is_paragraph_open :
						html += f'			</div> <!-- paragraph -->\n'
						is_paragraph_open = False
					


			# 제목
			for title in data['titles']:
				if title.get("location") == verse['location'] :
					title_class = ''
					if title.get('type') == "s" : title_class = 'subTitle'
					elif title.get('type') == "ms" : title_class = 'title'
					elif title.get('type') == "sp" : title_class = 'smallTitle'
					else : print(f"*** error: no type for title in {verse['location']}")

					html += f'			<div class="titleBox">\n'
					html += f'			<p class="{title_class}">{title['text']}</p>\n'

					# 레퍼런스
					for ref in data['references'] :
						if ref.get("location") == verse['location'] :
							html += f'			<p class="reference">('
							html_ref_verses = []
							for ref_verce in ref['verses'] :
								
								start_book_code = get_book_code(ref_verce['start'])
								start_chapter_num = get_chapter_num(ref_verce['start'])
								start_verse_num = get_verse_num(ref_verce['start'])

								end_book_code = get_book_code(ref_verce['end'])
								end_chapter_num = get_chapter_num(ref_verce['end'])
								end_verse_num = get_verse_num(ref_verce['end'])

								ref_html = f'<a href="{get_page_body_xhtml_name(start_book_code)}#{get_verse_id(start_book_code, start_chapter_num, start_verse_num)}">'

								if ref_verce['start'] == ref_verce['end'] :
									ref_html += f'{bible_info[start_book_code]['korean_concise_name']} {start_chapter_num}:{start_verse_num}'
								else :
									if start_chapter_num != end_chapter_num : 
										ref_html += f'{bible_info[start_book_code]['korean_concise_name']} {start_chapter_num}:{start_verse_num}-{end_chapter_num}:{end_verse_num}'
									else : ref_html += f'{bible_info[start_book_code]['korean_concise_name']} {start_chapter_num}:{start_verse_num}-{end_verse_num}'
								
								ref_html += '</a>'
								html_ref_verses.append(ref_html)
							html += "; ".join(html_ref_verses)
							html += ")"
							html += "</p>\n"
					
					html += f'			</div> <!-- titleBox -->\n'
					break
			
			for paragraph in data['paragraphs'] :
				if paragraph.get("location") == verse['location'] :
					html += f'			<div class="paragraph">\n'
					is_paragraph_open = True
			
			# 현재 절의 주석 위치에 각주 마크 삽입
			verse_footnotes = [
				fn for fn in chapter_footnotes
				if get_verse_num(fn['location']) == str(verse['num'])
			]
			verse["text"], footnoteIndex = insert_footnote_marks(
				verse["text"], verse["location"], verse_footnotes, footnoteIndex, collected_footnotes
			)

			verse["text"] = verse["text"].replace('\n', '<br/>')
			html += f'				<div class="verse" id="{get_verse_id(book_code, chapter_num, verse["num"])}"><p class="verseNum">{verse["num"]}</p><p class="verseText">{verse["text"]}</p></div>\n'

		if is_paragraph_open :
			html += f'			</div> <!-- paragraph -->\n'
			is_paragraph_open = False
		html += f'''		</div> <!-- content -->
		<div class="footnoteContent">
'''

		for footnoteIndex, footnote in collected_footnotes :
			html += f'			<div class="footnote"><a epub:type="footnote" class="footnoteNum" id="{get_end_footnote_id(footnote['id'])}" href="#{get_start_footnote_id(footnote['id'])}">{footnoteIndex})</a><p class="footnoteText">{footnote["text"]}</p></div>\n'

		testament_type = ''
		if bible_info[get_book_code(verse['location'])]['is_old_testament'] :
			testament_type = 'OldTestament'
		else :
			testament_type = 'NewTestament'


		html += f'''		</div> <!-- footnoteContent -->
	</div> <!-- section -->
	<div class="footer">
		<div class="footer{testament_type}ColoredBtn"><a href="{get_page_index_xhtml_name()}">성경</a></div>
		<div class="footerBtn"><a href="{get_page_chapter_index_xhtml_name(book_code)}">{bible_info[book_code]['korean_concise_name']}</a></div>
		<div class="footerBtn"><a href="#{get_chapter_id(book_code, chapter_num)}">{chapter_num}</a></div>
	</div> <!-- footer -->
	<div class="pagebreak"></div>
</div> <!-- chapter -->
'''
	
	# 파일 저장
	html += '\n</body>\n</html>'
	filename = f'pages/body/{get_page_body_xhtml_name(book_code)}'
	with open(filename, 'w', encoding='utf-8') as f:
			f.write(html)
	
	print(f'생성됨: {filename} ({book_name})')

print('\n완료! Sigil에서 HTML 파일들을 임포트하세요.')
import json

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

# id getter
def get_chapter_id(book_code, chapter_num) :
	return f'chapter_{book_code}_{chapter_num}'

# page name getter
def get_page_body_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}b_body{book_code}'

def get_page_body_xhtml_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}b_body_{book_code}.xhtml'

def get_page_chapter_index_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}a_chapter_index_{book_code}'

def get_page_chapter_index_xhtml_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}a_chapter_index_{book_code}.xhtml'
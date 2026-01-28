import json

with open('bible_info.json', 'r', encoding='utf-8') as f:
	bible_info = json.load(f)

def get_location(book_code, chapter_num, verse_num) :
	return f'{book_code}.{chapter_num}.{verse_num}'

def get_location_info(location) :
	return location.split('.')

def get_book_code(location) :
	return location.split('.')[0]

def get_chapter_num(location) :
	return location.split('.')[1]

def get_verse_num(location) :
	return location.split('.')[2]

# id getter
def get_verse_id(book_code, chapter_num, verse_num) :
	return f'verse_{book_code}_{chapter_num}_{verse_num}'

def get_chapter_id(book_code, chapter_num) :
	return f'chapter_{book_code}_{chapter_num}'

def get_GOS_id() :
	return 'GOS'

def get_start_footnote_id(id) :
	return f'footnote_start_{id}'
def get_end_footnote_id(id) :
	return f'footnote_end_{id}'

# page name getter
def get_page_body_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}b_body{book_code}'

def get_page_body_xhtml_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}b_body_{book_code}.xhtml'

def get_page_GOS_body_name() :
	return '67b_body_GOS'

def get_page_GOS_body_xhtml_name() :
	return '67b_body_GOS.xhtml'


def get_page_index_xhtml_name() :
	return '00_index.xhtml'

def get_page_chapter_index_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}a_chapter_index_{book_code}'

def get_page_chapter_index_xhtml_name(book_code) :
	return f'{'%02d'%int(bible_info[book_code]["order"])}a_chapter_index_{book_code}.xhtml'
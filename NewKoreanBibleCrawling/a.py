import json

with open('result2.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

# result3.json과 합치기
with open('result3.json', 'r', encoding='utf-8') as f:
	data3 = json.load(f)

# result3의 verses를 result2에 추가 (같은 location이 있으면 result3의 것으로 덮어쓰기)
verses_dict = {verse['location']: verse for verse in data['verses']}
for verse in data3['verses']:
	verses_dict[verse['location']] = verse
data['verses'] = list(verses_dict.values())

# result3의 titles를 result2에 추가
titles_dict = {title['location']: title for title in data.get('titles', [])}
for title in data3.get('titles', []):
	titles_dict[title['location']] = title
data['titles'] = list(titles_dict.values())

# result3의 paragraphs를 result2에 추가
paragraphs_dict = {para['location']: para for para in data.get('paragraphs', [])}
for para in data3.get('paragraphs', []):
	paragraphs_dict[para['location']] = para
data['paragraphs'] = list(paragraphs_dict.values())

# result3의 footnotes를 result2에 추가
footnotes_dict = {footnote['location']: footnote for footnote in data.get('footnotes', [])}
for footnote in data3.get('footnotes', []):
	footnotes_dict[footnote['location']] = footnote
data['footnotes'] = list(footnotes_dict.values())

# result3의 references를 result2에 추가
references_dict = {}
for ref in data.get('references', []):
	key = str(ref.get('verses', []))  # references는 verses 배열을 키로 사용
	references_dict[key] = ref
for ref in data3.get('references', []):
	key = str(ref.get('verses', []))
	references_dict[key] = ref
data['references'] = list(references_dict.values())

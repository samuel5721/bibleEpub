from dataclasses import dataclass
import json

with open('result2.json', 'r', encoding='utf-8') as f:
	data = json.load(f)

# with open('result3.json', 'r', encoding='utf-8') as f:
# 	data3 = json.load(f)

# # result3의 verses를 result2에 추가 (같은 location이 있으면 result3의 것으로 덮어쓰기)
# verses_dict = {verse['location']: verse for verse in data['verses']}
# for verse in data3['verses']:
# 	verses_dict[verse['location']] = verse
# data['verses'] = list(verses_dict.values())

# # result3의 titles를 result2에 추가
# titles_dict = {title['location']: title for title in data.get('titles', [])}
# for title in data3.get('titles', []):
# 	titles_dict[title['location']] = title
# data['titles'] = list(titles_dict.values())

# # result3의 paragraphs를 result2에 추가
# paragraphs_dict = {para['location']: para for para in data.get('paragraphs', [])}
# for para in data3.get('paragraphs', []):
# 	paragraphs_dict[para['location']] = para
# data['paragraphs'] = list(paragraphs_dict.values())

# # result3의 footnotes를 result2에 추가
# footnotes_dict = {footnote['location']: footnote for footnote in data.get('footnotes', [])}
# for footnote in data3.get('footnotes', []):
# 	footnotes_dict[footnote['location']] = footnote
# data['footnotes'] = list(footnotes_dict.values())

# # result3의 references를 result2에 추가
# references_dict = {}
# for ref in data.get('references', []):
# 	key = str(ref.get('verses', []))  # references는 verses 배열을 키로 사용
# 	references_dict[key] = ref
# for ref in data3.get('references', []):
# 	key = str(ref.get('verses', []))
# 	references_dict[key] = ref
# data['references'] = list(references_dict.values())


for verse in data['verses'] :
  
  if verse['id'] == 47867 and verse['location'] == '1CO.16.19' :
    print('found')
    verse['text'] = "속주 아시아에 있는 교회들이 여러분에게 안부를 전합니다. 아퀼라와 프리스카가 자기들의 집에서 모이는 교인들과 함께, 여러분에게 진심을 모아 안부를 전합니다."

for ref in data['references'] :
  if len(ref['verses']) == 0 :
    data['references'].remove(ref)

# 중복된 location을 가진 verse 제거 (위의 것으로 합침)
seen_locations = set()
verses_to_remove = []
for i, verse in enumerate(data['verses']):
  if verse['location'] in seen_locations:
    verses_to_remove.append(i)
  else:
    seen_locations.add(verse['location'])

# 역순으로 제거하여 인덱스 문제 방지
for i in reversed(verses_to_remove):
  data['verses'].pop(i)

# 중복된 location을 가진 paragraph 제거
seen_locations = set()
paragraphs_to_remove = []
for i, paragraph in enumerate(data['paragraphs']):
  if paragraph['location'] in seen_locations:
    paragraphs_to_remove.append(i)
  else:
    seen_locations.add(paragraph['location'])

# 역순으로 제거하여 인덱스 문제 방지
for i in reversed(paragraphs_to_remove):
  data['paragraphs'].pop(i)


for footnote in data['footnotes'] :
  if footnote['id'] == 47532 and footnote['location'] == 'ACT.16.19.0' :
    footnote['location'] = "1CO.16.19.71"
    break

with open("entitle_bible_context.json", "w", encoding="utf-8") as f:
	json.dump(data, f, ensure_ascii=False, indent=2)
from constants import bible_dictionary, bibleKeys

import json

with open("bible_info.json", "w", encoding="utf-8") as f:
	json.dump(bible_dictionary, f, ensure_ascii=False, indent=2)

with open("bible_series.json", "w", encoding="utf-8") as f:
	json.dump(bibleKeys, f, ensure_ascii=False, indent=2)
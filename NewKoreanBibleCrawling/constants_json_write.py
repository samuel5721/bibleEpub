from constants import bible_dictionary

import json

with open("constants.json", "w", encoding="utf-8") as f:
	json.dump(bible_dictionary, f, ensure_ascii=False, indent=2)
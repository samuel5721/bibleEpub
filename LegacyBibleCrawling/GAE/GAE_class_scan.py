from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
import os
import json

with open('./bible_info.json', 'r', encoding='UTF-8') as f:
    bible_info = json.load(f)

# def inject_dom_utils(driver, js_path="dom_utils.js"):
# 	js_code = None
# 	try:
# 		abs_path = os.path.join(os.path.dirname(__file__), js_path)
# 		with open(abs_path, "r", encoding="utf-8") as f:
# 			js_code = f.read()
# 	except Exception as e:
# 		print(f"유틸 로드 중 에러 발생생: {e}")
# 	if js_code:
# 		driver.execute_script(js_code)


def setup_driver():
	"""Selenium WebDriver 설정"""
	chrome_options = Options()
	# chrome_options.add_argument("--headless")  # 브라우저 창 숨기기
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--window-size=1920,1080")
	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=chrome_options)
	return driver


def collect_first_class_occurrences(driver, seen_classes, book_code, chapter):
	"""
	eb-container 내부에서 등장하는 모든 class의 최초 위치를 기록합니다.
	seen_classes는 {class_name: {location, tag, sample}} 형태의 누적 딕셔너리입니다.
	"""
	try:
		container = driver.find_element(By.CSS_SELECTOR, ".bible_read")
	except Exception:
		return

	elements = container.find_elements(By.CSS_SELECTOR, "[class]")

	for el in elements:
		class_attr = el.get_attribute("class") or ""
		class_names = [c for c in class_attr.split() if c]
		# 공백이거나, 온점(.)이 포함된 클래스명만 있는 경우는 스킵
		class_names = [c for c in class_names if "." not in c]
		if not class_names:
			continue

		location = f'{book_code}, {chapter}'

		sample_text = (el.text or "").strip()
		if len(sample_text) > 80:
			sample_text = sample_text[:77] + "..."

		for cls in class_names:
			if cls in seen_classes:
				continue
			seen_classes[cls] = {
				"location": location,
				"tag": el.tag_name,
				"sample": sample_text
			}


def main():
	driver = setup_driver()
	wait = WebDriverWait(driver, 10)
	all_class_first_occurrences = {}

	try:
		for book_code, testament in bible_info.items():
			for i in range(testament["chapter_num"]):
				chapter = i + 1
				url = f"https://bskorea.or.kr/bible/korbibReadpage.php?version=SAE&book={book_code}&chap={chapter}"

				driver.get(url)
				print(f"페이지 로드 완료: {driver.title}, {book_code}, {chapter}")
				wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
				# inject_dom_utils(driver)
				time.sleep(0.1)

				collect_first_class_occurrences(driver, all_class_first_occurrences, book_code, chapter)

	except Exception as e:
		print(f"에러 발생: {e}")
	finally:
		with open("HAN_class_first_occurrences.json", "w", encoding="utf-8") as f:
			json.dump(all_class_first_occurrences, f, ensure_ascii=False, indent=2)
		driver.quit()


if __name__ == "__main__":
	main()

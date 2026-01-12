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

from constants import bible_dictionary

def inject_dom_utils(driver, js_path="dom_utils.js"):
    js_code = None
    try:
        abs_path = os.path.join(os.path.dirname(__file__), js_path)
        with open(abs_path, "r", encoding="utf-8") as f:
            js_code = f.read()
    except Exception:
        print(f"유틸 로드 중 에러 발생생: {Exception}")
    driver.execute_script(js_code)

def is_verse_num(element) :
	return "verse-span" in (element.get_attribute("class") or "") and element.find_elements(By.CSS_SELECTOR, ".v")

def is_footnote(object) :
	return len(object.find_elements(By.XPATH, "./*[contains(@class, 'ftext hidden')]")) > 0

# 절 본문 가져오기
def get_verce_texts(driver) :
	verses = driver.find_elements(By.CLASS_NAME, "verse-span")
	verse_nums = driver.find_elements(By.CSS_SELECTOR, ".verse-span:has(> .v)")
	return [i for i in verses if i not in verse_nums]

def get_titles(driver) :
	return driver.find_elements(By.CSS_SELECTOR, ".ms, .s")

def get_references(driver) :
	return driver.find_elements(By.CSS_SELECTOR, ".mr, .r")

def get_paragraphs(driver) :
	return driver.find_elements(By.CSS_SELECTOR, ".p, .m")

def get_quotes(driver) :
	return driver.find_elements(By.CLASS_NAME, "q1")

def get_footnotes(driver) :
	return driver.find_elements(By.CSS_SELECTOR, "[class*='ftext hidden']")

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

def main():

	# p, m 단락
	# q1 인용
	# ms 대제목
	# s 소제목
	# mr 대제목의 레퍼런스절
	# r 소제목의 레퍼런스절

	# p, m, q1 > verse-span > v : 절
	# p, m, q1 > verse-span : 본문
	# p, m, q1 > ft 서.장.절 > ftext hidden : 각주
	
	driver = setup_driver()
	wait = WebDriverWait(driver, 10)
	
	try:
		all_verse_maps = []
		all_title_maps = []
		all_reference_maps = []
		all_paragraph_maps = []
		all_footnote_maps = []

		for name, testament in bible_dictionary.items() :
			for i in range(testament["chapter_num"]) :
				chapter = i + 1
				url = f"https://www.bskorea.or.kr/KNT/index.php?chapter={name}.{chapter}"

				driver.get(url)
				print(f"페이지 로드 완료: {driver.title}")
				# 페이지 로드 대기
				wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
				inject_dom_utils(driver)
				time.sleep(0.1)

				# 이 장에서 사용할 WebElement 들만 가져오기
				ch_verse_texts = get_verce_texts(driver)
				ch_titles = get_titles(driver)
				ch_references = get_references(driver)
				ch_paragraphs = get_paragraphs(driver)
				ch_footnotes = get_footnotes(driver)

				# 절 본문 전처리
				ch_verse_maps = []
				temp_source = None
				temp_text = None
				for verse_text in ch_verse_texts:
					now_source = verse_text.get_attribute("data-verse-id")
					if temp_source == now_source:
						#만약 이 절이 인용구라면 앞에 개행을 추가한다.
						if "q1" in verse_text.find_element(By.XPATH, "..").get_attribute("class").split():
								temp_text += '\n'
						temp_text += verse_text.get_attribute("textContent")
					else:
						ch_verse_maps.append({'id': temp_source, 'text': temp_text})
						temp_source = now_source
						temp_text = verse_text.get_attribute("textContent")

				# 첫 번째 dummy(None) 제거 및 마지막 절 추가
				if len(ch_verse_maps) > 0:
					ch_verse_maps.pop(0)
				if temp_source is not None and temp_text is not None:
					ch_verse_maps.append({'id': temp_source, 'text': temp_text})

				# verse_maps는 구절 본문을 저장하며
				# id: 서명.장.절
				# text: 그 절의 내용
				# 으로 하는 딕셔너리의 리스트입니다.
				# [ ... {'id': 'GEN.5.32', 'text': ' 노아는 500세가 되어 셈, 함, 야벳을 낳았다.'} ... ]
				# 인용되어 개행한 후 들여쓰기 된 구절은 \n을 통해 표현하였습니다.
				all_verse_maps.extend(ch_verse_maps)

				# 제목 전처리
				ch_title_maps = []
				for title in ch_titles:
					# 바로 뒤에 오는 형제 요소의 자식 중 verse-span인 요소를 찾습니다.
					next_sibling = title.find_element(By.XPATH, "following-sibling::*[.//*[contains(@class,'verse-span')]][1]")
					child = next_sibling.find_element(By.CLASS_NAME, "verse-span")

					source = child.get_attribute("data-verse-id")
					text = title.get_attribute("textContent")
					title_type = title.get_attribute("class")
					ch_title_maps.append({'id': source, 'text': text, 'type':title_type})
				
				# title_maps는 제목을 저장하며
				# id: 자신 바로 뒤에 나오는 구절의 서명.장.절
				# text: 제목의 내용
				# type: 제목의 유형(ms: 대제목, s: 소제목)
				# 으로 하는 딕셔너리의 리스트입니다.
				# [{'id': 'GEN.1.1', 'text': '하나님이 온 누리를 지으시다', 'type': 's'}, ...
				all_title_maps.extend(ch_title_maps)

				# 레퍼런스 전처리
				ch_reference_maps = []
				for reference in ch_references :
					# 바로 뒤에 오는 형제 요소의 자식 중 verse-span인 요소를 찾습니다.
					next_sibling = reference.find_element(By.XPATH, "following-sibling::*[.//*[contains(@class,'verse-span')]][1]")
					child = next_sibling.find_element(By.CLASS_NAME, "verse-span")

					inner_references = reference.find_elements(By.XPATH, "./*")

					source = child.get_attribute("data-verse-id")
					reference_type = reference.get_attribute("class")

					addrs = []
					for inner_reference in inner_references :
						ref_id = inner_reference.get_attribute("id")
						if ref_id and '-' in ref_id:
							parts = ref_id.split('-')
							if len(parts) >= 2:
								start_point = parts[0]
								end_point = parts[1]
								addrs.append({'start': start_point, 'end':end_point})

					ch_reference_maps.append({'id': source, 'type':reference_type, 'verses':addrs})
				all_reference_maps.extend(ch_reference_maps)

				# 단락 전처리
				ch_paragraph_maps = []
				for paragraph in ch_paragraphs:
					child = paragraph.find_element(By.CLASS_NAME, "verse-span")

					source = child.get_attribute("data-verse-id")
					paragraph_type = paragraph.get_attribute("class")
					ch_paragraph_maps.append({'id': source, 'type':paragraph_type})
				
				# paragraph_maps는 구절들의 집합인 단락을 저장하며, 
				# id: 단락 안에서 처음 나오는 구절의 서명.장.절
				# type: 단락의 유형
				# 	단락의 종류는 p, m이 있습니다. p는 평범한 본문들의 집합입니다. m은 q1 이후 나타나는 단락으로, p와 차이점은 없어 보입니다.
				# 으로 하는 딕셔너리의 리스트입니다.
				# [{'id': 'GEN.1.1', 'type': 'p'}, {'id': 'GEN.1.6', 'type': 'p'}, {'id': 'GEN.1.9', 'type': 'p'} ...
				
				all_paragraph_maps.extend(ch_paragraph_maps)

				# 각주 전처리
				ch_footnote_maps = []
				for footnote in ch_footnotes:
					footnote_id = footnote.get_attribute("id")
					if not footnote_id or '.' not in footnote_id:
						continue
					parts = footnote_id.split(".", 1)
					if len(parts) < 2:
						continue
					verse_source = parts[1]

					# 각주 앞에 글자가 몇 개 있는지 검사하는 코드
					char_source = driver.execute_script(
						"return window.BibleDOM.getCharOffsetBeforeFootnote(arguments[0]);",
						footnote
					)
					# dbg = driver.execute_script(
					# 		"return window.BibleDOM.debugFootnote(arguments[0]);",
					# 		footnote
					# )

					source = verse_source + "." + str(char_source)
					text = footnote.get_attribute("textContent")
					ch_footnote_maps.append({'id': source, 'text': text})
				
				# footname_maps는 각주를 저장하며
				# id: 구절의 서명.장.절.{자신이 나오기 전 해당 절의 글자 수}
				# text: 각주의 내용
				# GEN.1.2.39 각주는 창세기 1장 2절의 39글자(띄어쓰기 포함) 이후 각주가 나타난다는 뜻입니다.
				# {'id': 'GEN.1.1.0', 'text': '또는 ‘태초에’'}, {'id': 'GEN.1.2.39', 'text': '또는 ‘하나님의 바람’'} ...
				all_footnote_maps.extend(ch_footnote_maps)

	except Exception as e:
		print(f"에러 발생: {e}")
	finally:
		json_output = {
			"verses": all_verse_maps,
			"titles": all_title_maps,
			"references": all_reference_maps,
			"paragraphs": all_paragraph_maps,
			"footnotes": all_footnote_maps
		}


		with open("result.json", "w", encoding="utf-8") as f:
				json.dump(json_output, f, ensure_ascii=False, indent=2)

		driver.quit()

if __name__ == "__main__":
	main()


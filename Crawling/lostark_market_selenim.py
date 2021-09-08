from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import pyperclip
import pyautogui

craftclass_dict = {'배틀아이템':30411,
                  '요리':30200,
                  '특수':30700}

# 인벤에서 제작 데이터 획득
def get_data_craft(craftclass):
    # 옵션 생성
    options = webdriver.ChromeOptions()

    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    # mac Chrome (brew로 chromedriver 설치한 경우)
    driver = webdriver.Chrome(options=options)

    # 사이트 이동
    driver.get(f'https://lostark.inven.co.kr/dataninfo/craft/?craftclass={craftclass}')

    # 대기
    driver.implicitly_wait(1)

    # HTML 데이터 가져오기
    req = driver.page_source

    # driver 종료
    driver.quit()

    # BeautifulSoup HTML 파싱
    soup = BeautifulSoup(req, 'html.parser')
    # print(soup)

    # 특정 구간 데이터 선택
    html_tables = str(soup.select("#lostarkDb > div.lostark.db_board.db_craft > table"))

    # pandas tables 변환
    pd_tables = pd.read_html(html_tables)
    # print (pd_tables)

    # pandas 데이터 생성
    df = pd.DataFrame(pd_tables[0], columns=['결과물', '필요재료', '상세정보'])

    # 불필요한 데이터 삭제
    searchList = ['등록된 정보가 없습니다.']
    df = df[-df['결과물'].str.contains('|'.join(searchList))]
    return df


# 로아 마켓 데이터 획
def get_data_market(item_name):
    # 옵션 생성
    options = webdriver.ChromeOptions()

    # 창 숨기는 옵션 추가
    # options.add_argument("headless")

    # mac Chrome (brew로 chromedriver 설치한 경우)
    driver = webdriver.Chrome(options=options)

    # 사이트 이동
    driver.get('https://lostark.game.onstove.com/Market')

    # 대기
    driver.implicitly_wait(3)

    # 로그인 버튼 클릭
    XPATH_BUTTON = '//*[@id="naver_login"]/i'
    btn_search = driver.find_element_by_xpath(XPATH_BUTTON)
    btn_search.click()

    # 로그인 창 변경
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)

    # id, pw 입력할 곳을 찾습니다.
    tag_id = driver.find_element_by_name('id')
    tag_pw = driver.find_element_by_name('pw')

    # id 입력
    time.sleep(1)
    # tag_id.click()
    pyautogui.typewrite('czend', interval=1)
    pyautogui.press('tab')
    pyautogui.typewrite('Zestys55!$15', interval=1)
    pyautogui.press('enter')

    # 로그인 창 변경
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)

    # 로그인 엔터
    # 버튼 클릭 방법2
    # XPATH_BUTTON = '//*[@id="log.login"]'
    # btn_search = driver.find_element_by_xpath(XPATH_BUTTON)
    elem = driver.find_element_by_id("log.login")
    elem.click()

    # 종료
    # driver.quit()
    # driver.switch_to.window(driver.window_handles[1])

    # 대기
    time.sleep(100)

    return


    # 크롤링 사이즈 검색
    # assert "로스트아크 - 거래소" in driver.title
    elem = driver.find_element_by_id("txtItemName")
    elem.send_keys(item_name)

    # 버튼 클릭 방법1
    # elem.send_keys(Keys.RETURN)

    # 버튼 클릭 방법2
    XPATH_BUTTON = '//*[@id="lostark-wrapper"]/div/main/div/div[2]/div[2]/form/fieldset/div/div[4]/button[1]'
    btn_search = driver.find_element_by_xpath(XPATH_BUTTON)
    btn_search.click()

    # HTML 데이터 가져오기
    req = driver.page_source

    # driver 종료
    driver.quit()

    # BeautifulSoup HTML 파싱
    soup = BeautifulSoup(req, 'html.parser')

    # 특정 구간 데이터 선택
    html_tables = str(soup.select("#itemList"))

    # pandas tables 변환
    pd_tables = pd.read_html(html_tables)
    # print (pd_tables)

    # pandas 데이터 생성
    df = pd.DataFrame(pd_tables[0], columns=['등급', '전일 평균 거래가', '최근 거래가', '최저가'])
    return df


# 아이템 목록 파싱
def parser_item_list(text):
    # 수량 데이터 획득
    numbers = re.findall("\d+", text)
    # print(numbers)

    # 아이템 목록 분리
    item_list = text.split('x')
    # print(item_list)

    item_dict = dict()
    for key, item in enumerate(item_list):

        # 숫자 데이터 삭제
        p = re.compile("[^0-9]")
        item = "".join(p.findall(item)).strip()

        # 빈 문자열 체크
        if not item:
            continue

        # 사전에 데이 추가
        item_dict[item] = numbers[key]
        # print(item_dict)
        # print(key, item, numbers[key])

    # print(item_dict)
    return item_dict


# 거래소에서 가격 데이터 획득
items_price = get_data_market('회복약')
print(items_price)



# 제작 데이터 조회 및 획득
items_craft1 = get_data_craft(craftclass_dict['배틀아이템'])
items_craft2 = get_data_craft(craftclass_dict['특수'])
items_craft_all = pd.concat([items_craft1, items_craft2], ignore_index=True)

# 제작 데이터 변환 (df to dict)
items_craft_dict = items_craft_all.to_dict('index')
# items_craft_list = items_craft.to_dict('list')
# items_craft_list = items_craft.set_index('결과물').T.to_dict('list')
# print((items_craft_dict))


for key in items_craft_dict:
    item_list = parser_item_list(items_craft_dict[key]['필요재료'])
    # print(key, items_craft_dict[key]['결과물'], item_list)
    # 가격 검색
    # item_price = get_data_market(key)
    print(f'제품:{key}')


# for item_info in items_craft_dict:
#     print(item_info)

# item_list = items_craft_dict.items()
# for item in item_list:
# print(item.get('결과물'))
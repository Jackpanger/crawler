from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchWindowException
from config import *
import time
import re
from pyquery import PyQuery as pq
from datetime import datetime,timedelta
import json
from multiprocessing import Pool
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Chrome()

wait = WebDriverWait(browser,10)

def both():
    global i
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#pageList > ul > li:nth-child({}) > span'.format(i))))
    JUdge = judge(input.text)
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#pageList > ul > li:nth-child({}) > a'.format(i))))
    submit.click()
    browser.window_handles
    browser.switch_to.window(browser.window_handles[1])
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#example')))
    get_products()
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    i += 1



def search():
    try:
        global i,sure,offset
        if 0 <offset < 9:
            url = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index' + str(offset) + '.html'
            browser.get(url)
            both()
            if i == 31:
                browser.quit()
        elif offset == 0 :
            url = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index.html'
            browser.get(url)
            both()
            if i == 31:
                browser.quit()
        elif offset == 9 :
            url = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index9.html'
            browser.get(url)
            both()
            if i == 31:

                browser.quit()
        else:
            url = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index9.html'
            input = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#pageList > div > ul > li:nth-child({}) > a'.format(offset + 2))))
            input.click()
            both()
            if not JUdge:
                print(JUdge)
                submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#pageList > ul > li:nth-child({}) > a'.format(i))))
                submit.click()
                browser.window_handles
                browser.switch_to.window(browser.window_handles[1])
                total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#example')))
                get_products()
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                i += 1
                if i == 31:
                    next_page(offset)
                    i = 1
                print(i)
            else:
                print('finished')
                browser.quit()
                sure = False
    except TimeoutException:
        return search()



def judge(time):
    a = datetime.now()
    b = datetime(a.year -1, a.month, a.day -1).strftime("%Y.%m.%d")
    if int(time[0:4]) <= a.year-1 and int(time[5:7]) <= a.day and int(time[8:10])<=a.day:
        return True
    else:
        return False


def next_page(offset):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '# pageNum')))
        input.clear()
        input.send_keys('{}'.format(offset+2))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#form2 > a')))
        submit.click()

    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#example')))
    html = browser.page_source
    doc = pq(html)
    items = doc ('#example').items()
    for item in items:
        product = {
            'title':item.find('#ivs_title').text(),
            'time':item.find('#ivs_date').text().strip('()'),
            'source': item.find('.PBtime').text()[27:].strip(),
            'content':item.find('#ivs_content').text(),
        }
    with open('data.txt','a',encoding = 'utf-8') as f:
        f.write(json.dumps(product, ensure_ascii=False,)+'\n')
i = 1
offset = 1
def main():

    sure = True

    while sure:
        search()



if __name__ == '__main__':
    # pool = Pool(3)
    # for i in range(30):
    #     pool.apply_async(main,(i-1,))
    main()

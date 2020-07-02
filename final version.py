from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium import webdriver
from pyquery import PyQuery as pq
import time

#设置chromedriver
aulr = r'C:\Users\YJC\AppData\Local\Google\Chrome\Application\chromedriver'
browser = webdriver.Chrome()
#设置超时时间

wait = WebDriverWait(browser,10)
arr = []
dic = {}

def get_url():
    for x in range(1,2):
        try:
            y = x-1
            if y==0:
                y = ''
                pass
            #打开网页
            url = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index'+str(y)+'.html'
            browser.get(url)
            # time.sleep(5)
            # js = 'window.scrollTo({ top: 1000, behavior: "smooth" });'
            # browser.execute_script(js)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pageList')))
            #打印网页内容
            soup =BeautifulSoup(browser.find_element_by_css_selector('#pageList').get_attribute('innerHTML'),features="lxml")
            for z in soup.find('ul',attrs={'class':'uli14 pageList'}).findAll('a'):
                arr.append(z.get('href'))
                pass
            time.sleep(1)
        except TimeoutException:
            return get_url()


def get_products():

    for x in arr:
        try:
            browser.get('http://www.shanghai.gov.cn' + x)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#example')))
            html = browser.page_source
            doc = pq(html)
            items = doc('#example').items()
            for item in items:
                product = {
                    'title': item.find('#ivs_title').text(),
                    'time': item.find('#ivs_date').text().strip('()'),
                    'source': item.find('.PBtime').text()[27:].strip(),
                    'content': item.find('#ivs_content').text(),
                }
            with open('data.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(product, ensure_ascii=False ) + '\n')
            time.sleep(1)
        except TimeoutException:
            return get_products()
    browser.close()

def main():
    get_url()
    get_products()

if __name__ == '__main__':
    main()


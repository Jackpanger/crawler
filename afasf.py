import urllib
import re
import time
from bs4 import BeautifulSoup
import json


if __name__ == '__main__':
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    arr = []
    #设置chromedriver
    aulr = r'C:\Users\YJC\AppData\Local\Google\Chrome\Application\chromedriver'
    browser = webdriver.Chrome()
    #设置超时时间
    browser.set_page_load_timeout(10)
    for x in range(1,3):
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
            element = WebDriverWait(browser, 10).until(lambda x:x.find_element_by_css_selector('#pageList'))
            #打印网页内容
            soup =BeautifulSoup(browser.find_element_by_css_selector('#pageList').get_attribute('innerHTML'),features="lxml")
            print(soup.find('ul',attrs={'class':'uli14 pageList'}).findAll('a'))
            print(type(soup.find('ul',attrs={'class':'uli14 pageList'}).findAll('a')))
            for z in soup.find('ul',attrs={'class':'uli14 pageList'}).findAll('a'):
                arr.append(z.get('href'))
                pass
            time.sleep(5)

        except:
            print('错误123')
    print(arr)
    dic = {}
    for x in arr:
        try:
            browser.get('http://www.shanghai.gov.cn' + x)
            dic['title'] = browser.find_element_by_css_selector('#ivs_title').text
            dic['date'] = browser.find_element_by_css_selector('.PBtime').text.split('\n\n')[0]
            dic['source'] = browser.find_element_by_css_selector('.PBtime').text.split('\n\n')[1].replace('来源：', '')
            dic['content'] = browser.find_element_by_css_selector('#ivs_content').get_attribute('innerHTML')
            # print(dic)

            time.sleep(5)
        except:
            print("正确")
    with open('data.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False, ) + '\n')

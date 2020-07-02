from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from config import *
import time
from pyquery import PyQuery as pq
from configs import *
import os
import pickle
import requests

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_options)
# options = webdriver.ChromeOptions()
# prefs = {"":""}
# prefs["credentials_enable_service"] = False
# prefs["profile.password_manager_enabled"] = False
# options.add_experimental_option("prefs", prefs)
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
# browser = webdriver.Chrome(chrome_options=options)
# wait = WebDriverWait(browser,10)
# browser.maximize_window()


def search():
    try:
        r = requests.get('https://ice.xjtlu.edu.cn/')
        print(r.json())
        users = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#username')))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#password')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#loginbtn')))
        users.send_keys('jinhao.pang18')
        # time.sleep(2)
        password.send_keys('Xcdlnrhhz2')
        # time.sleep(2)
        submit.click()
        cookies = browser.get_cookies()  # 获取cookies信息
        # [{'domain': 'baidu.com', 'expiry': 2145916555, 'httpOnly': False, 'name': 'BAIDUID', 'path': '/', 'secure': False, 'value': '7100184EE9148BA1781E8E646A39AAC1:FG=1'}, {'httpOnly': False, 'name': 'BD_HOME', 'secure': False, 'value': '0'}, {'httpOnly': False, 'name': 'BD_LAST_QID', 'secure': False, 'value': '14145111259049246984'}, {'domain': 'www.baidu.com', 'expiry': 1559080787, 'httpOnly': False, 'name': 'BD_UPN', 'path': '/', 'secure': False, 'value': '1123314351'}, {'domain': 'baidu.com', 'expiry': 2565768663, 'httpOnly': False, 'name': 'BIDUPSID', 'path': '/', 'secure': False, 'value': 'BAFCB5C72B0C5D1C55D4086B1DD4BCE1'}, {'httpOnly': False, 'name': 'H_PS_PSSID', 'secure': False, 'value': '1449_21085_29063_28519_28769_28722_28963_28837_28584_28703'}, {'domain': 'baidu.com', 'expiry': 2145916555, 'httpOnly': False, 'name': 'PSTM', 'path': '/', 'secure': False, 'value': '1556616664'}, {'httpOnly': False, 'name': 'delPer', 'secure': False, 'value': '0'}]

        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        # total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        # get_products()
        return 1
    except TimeoutException:
        return search()

def choose_course():
    try:

        ex = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#block-myoverview-5e3e9a047dffa5e3e9a047c6723')))
        print(ex)
        js = 'window.scrollTo(0,10000)'
        browser.execute_script(js)
        path = '#course-info-container-293-7 > div > div.w-100.text-truncate > a'
        choose = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,path)))
        choose.click()
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc ('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find(',shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败，result')

def main():
    # total = search()
    # total = int(re.compile('(\d+)').search(total).group(1))
    # for i in range(2,total +1):
    #     next_page(i)
    # getTaobaoCookies()
    search()
    # time.sleep(2)
    # choose_course()
    # browser.close()

if __name__ == '__main__':
    main()

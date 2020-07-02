# import requests
# # from pyquery import PyQuery as pq
# #
# # url = 'https://www.zhihu.com/explore'
# # headers = {
# #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# # }
# # html = requests.get(url, headers=headers).text
# # doc = pq(html)
# # items = doc('.explore-tab .feed-item').items()
# # for item in items:
# #     question = item.find('h2').text()
# #     author = item.find('.author-link-line').text()
# #     answer = pq(item.find('.content').html()).text()
# #     file = open('explore.txt', 'a', encoding='utf-8')
# #     file.write('\n'.join([question, author, answer]))
# #     file.write('\n' + '=' * 50 + '\n')
# #     file.close()
import requests #网络请求
import re #正则表达式,提取数据
import pandas #数据分析模块
import time
from selenium import webdriver
browser = webdriver.Chrome()
for ii in range(1):#实现翻页
    mn = 44*(ii-1)
    url = 'https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171223&ie=utf8&psort=_lw_quantity&vlist=1&app=vproduct&cps=yes&cd=false&v=auction&tab=all&bcoffset=3&ntoffset=0&p4ppushleft=1%2C48&s='+str(mn)
    browser.get('https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20171223&ie=utf8&psort=_lw_quantity&vlist=1&app=vproduct&cps=yes&cd=false&v=auction&tab=all&bcoffset=3&ntoffset=0&p4ppushleft=1%2C48&s='+str(mn))
    #加快执行效率
    print(browser.page_source)
    ren = re.compile('"raw_title":"(.*?)","pic_url":"(.*?)","detail_url":".*?","view_price":"(.*?)","view_fee":"(.*?)","item_loc":"(.*?)","view_sales":"(.*?)人付款","comment_count":"(.*?)","user_id":"(.*?)","nick":"(.*?)"')
    data =re.findall(ren,html.text)

    data2 =pandas.DataFrame(data) #转化数据框

    data2.to_csv(r'D:\TBB.csv',header=False,index=False,mode='a+')#写成csv文件,并且追加
    time.sleep(1)
#数据块
# import pandas
# import matplotlib as mpl #字体模块
# import matplotlib.pyplot as plt #绘图模块
#
# mpl.rcParams["font.sans-serif"] = ['SimHei']#配置字体
# #绘图格式
# plt.rcParams["axes.labelsize"] = 16
# plt.rcParams["xtick.labelsize"] =15
# plt.rcParams["ytick.labelsize"] =10
# plt.rcParams["legend.fontsize"]=10#图例字体大小
# plt.rcParams["figure.figsize"]=[15,12]
# def1 =pandas.read_csv('D:\TBB.csv',engine='python')
# TBdata = pandas.DataFrame(list(zip(def1['I'],def1['F']*def1['C'])))
# #可视化
# DD = TBdata.groupby([0]).sum()
# DD[1].plot(kind='bar',rot=90)
# DD[1].plot(rot=90)#底下标旋转90度
# plt.show()
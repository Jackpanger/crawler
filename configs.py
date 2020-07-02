import requests
from pyquery import PyQuery as pq
import json
r = requests.get('http://www.shanghai.gov.cn/nw2/nw2314/nw2315/nw4411/index.html')
print(r.text)
doc = pq(r.text)
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
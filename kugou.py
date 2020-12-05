import requests

star = input("输入你要搜索的内容: \n")
number = input("输入下载第几页，不输入默认下载第一页，输入全部下载全部:\n")

if number == "全部":
    continueNum = "0"
else:
    if not number:
        number = "1"
    continueNum = str(input("输入下载几页, 0代表余下的都下载: \n"))

while True:
    url = "https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&httpsStatus=1&reqId=1528bac0-03ca-11eb-b45e-2386c1a09b6b".format(star,number)
    headers = {
        "Cookie": "_ga=GA1.2.2013567128.1601544837; _gid=GA1.2.309397512.1601544837; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1601544837,1601545194; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1601545194; kw_token=VASJ7SMONR",
        "csrf":"VASJ7SMONR",
        # "Host": "www.kuwo.cn",
        "Referer": "https://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    }
    response = requests.get(url, headers = headers).json()
    if response['code'] == -1:
        break
    data = response['data']['list']
    # print(response)
    for i in data:
        rid = i['rid']
        name = i["name"]
        # print(rid,name)
        new_url = "https://www.kuwo.cn/url?format=mp3&rid="+str(rid)+"&response=url&type=convert_url3&br=128kmp3&from=web&t=1601546519809&httpsStatus=1&reqId=258cde20-03cd-11eb-bf15-27cbd345da42"
        res = requests.get(new_url).json()
        # print(res['url'])
        result = requests.get(res['url']).content
        path = "酷我音乐\\"+ name +".mp3"
        with open(path,"wb") as f:
            f.write(result)
            print("正在下载： ",name)

    if continueNum != 0 :
        if continueNum == 1:
            break
        else:
            number= str(int(number)+1)
            continueNum -= 1
print("全部下载完成")
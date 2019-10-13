import re
import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
import random
import cableAR
import datetime
from operator import itemgetter

# 找到电视剧/综艺的主板面，进行数据提取和清洗
# 进行名字对比，有需要的电视剧/综艺名字与对齐的所属电视台和数据留下/BeautifulSoup
# 对名称进行排行，同时改变其他相对变量的排名
# 查找上一期并做对比
# 先是名称对比，寻找对应的中文翻译，再对数据进行对比
# 按格式输出
# 分类解决问题，如，一周内仅一天播放的节目，两天连起来播放的节目

def set_ip():
    # ip list
    iplist = ['45.125.32.181', '125.123.64.234', '58.22.212.39', '171.11.179.77','125.123.126.185','125.123.123.114','58.22.213.30']
    # create an opener
    proxy_support = urllib.request.ProxyHandler({'http': iplist[random.randint(0, len(iplist) - 1)]})
    opener = urllib.request.build_opener(proxy_support)

    # create a disguise header
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')]
    return opener

#requst html
def req_html(opener, url):
    # use opener to request url
    response = opener.open(url)
    # read response and decode it
    html = response.read().decode('utf-8')
    return html

# 搜集表格信息
def correct_table(html):
    soup = BeautifulSoup(html,'html.parser')
    ll = soup.find_all('tbody')
    ll = str(ll)
    #print(ll)
    infolist = []
    result = re.findall(r'<tr>(.*?)</tr>', ll)
    #print(result)
    for i in result:
        #print(i)
        fir = re.findall(r'urlencode.*?this.href.*?;">(.*?)</p>',i)
        res = re.findall(r'<p class="rate">(.*?)</p></td>',i)
        if len(res) == 0:
            res = re.findall(r'<p class="rate n123">(.*?)</p></td>',i)
        fir = fir + res
        #print(fir)
        infolist.append(fir)
    return infolist

# 对表格信息进行过滤
def clean_infolist(infolist):
    #>>> sorted(d, key = lambda x:x[1]) 多维列表二列排序
    #>>> sorted(d) 多维列表与单维列表的首位升序排序
    print()
    newlist = []
    for i in range(0, len(infolist)):
        print(infolist[i][0])
        res = infolist[i][0].find('(재방송)')
        if res == -1:
            temp = infolist[i]
            temp[0] = temp[0].strip('</a>')
            temp[1] = temp[1].strip('</a>')
            #print(temp)
            newlist.append(temp)
    #print()
    return newlist

# 返回当日日期，integer格式
def build_search_obj():
    lctime = cableAR.find_localtime()
    month = int(lctime[5:7])
    day = int(lctime[8:10])-1
    date = [month, day]
    return date

# 返回搜索对象
def build_url(date,judge):
    str = ""
    if judge == 0:
        str = "드라마시청률"
        print(str(date[0]) + "月"+str(date[1])+"日电视剧收视率")
    else:
        str = "예능시청률"
        print(str(date[0]) + "月" + str(date[1]) + "日综艺收视率")
    str = str(date[0])+"월"+str(date[1])+"일"+str
    print(str)
    return str

# 日期不同所进行的拼凑的数据不同
def build_audlist(kr, yes, lstwk):
    # 对比名字，若是出现了则
    infolist = [[],[],[],[],[],[],[]]
    number = 0
    for i in range(0, len(yes)):
        if yes[i][0].find(kr) != -1:
            if yes[i][0].find("1부") != -1:
                infolist[1] = yes[i]
                number = 1
            elif yes[i][0].find("2부") != -1:
                infolist[2] = yes[i]
                number =2
            elif yes[i][0].find("3부") != -1:
                infolist[3] = yes[i]
                number = 3
    for i in range(0, len(lstwk)):
        if lstwk[i][0].find(kr) != -1:
            if lstwk[i][0].find("1부") != -1:
                infolist[4] = lstwk[i]
                number = 1
            elif lstwk[i][0].find("2부") != -1:
                infolist[5] = lstwk[i]
                number =2
            elif lstwk[i][0].find("3부") != -1:
                infolist[6] = lstwk[i]
                number = 3
    temp = [number]
    infolist[0] = temp
    return infolist

def build_all(ch, arst, infolist):
    pass
# 寻找上周的日期
def lst_date():
    now_time = datetime.datetime.now()
    # 选择要提前的天数
    change_time = now_time + datetime.timedelta(days=-8)
    # 格式化处理
    month = change_time.strftime('%m')
    day = change_time.strftime('%d')
    date = [int(month), int(day)]
    return date

def station_drama(weekday):
    drama_list = [['《#浪客行#》'],
                  [],
                  [],
                  [],
                  [],
                  ['《#秘密精品店#》'],
                  []]

    drama_kr = [['배가본드'],
                  [],
                  [],
                  [],
                  [],
                  ['시크릿부티크'],
                  []]

    drama_arst = [['（主演：#李昇基#、 #裴秀智#、 #申成禄#）'],
                  [],
                  [],
                  [],
                  [],
                  ['（主演：#金宣儿#、 #金宰英#、 #张美姬#）'],
                  []]
    lend = len(drama_list[weekday])
    lctime = cableAR.find_localtime()
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
    date = build_search_obj()
    yes_url = url + urllib.parse.quote(build_url(date))
    date = lst_date()
    lst_url = url + urllib.parse.quote(date)
    opener = cableAR.set_ip()
    lst_html = req_html(opener, lst_url)
    opener = set_ip()
    yes_html = req_html(opener, yes_url)
    for i in range(0, lend):
        # 昨天
        yes_infolist = correct_table(yes_html)
        yes_infolist = clean_infolist(yes_infolist)

        # 上周
        lst_infolist = correct_table(lst_html)
        lst_infolist = clean_infolist(lst_infolist)

if __name__ == '__main__':
    weekday = cableAR.decide_day()

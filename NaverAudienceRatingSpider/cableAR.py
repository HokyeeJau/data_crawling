import urllib
import urllib.request
import random
import re
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, date
# set IP and proxy
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

def find_title(html):
    pattern = re.compile(r'<h4><a nocr onclick=.*? target="_blank">(.*?)</a></h4>')
    title = pattern.findall(html)
    return title

def find_audratio(html):
    pattern = re.compile(r'class="graph_num">(.*?)</em>')
    audr = pattern.findall(html)
    return audr

def find_episode(html):
    pattern = re.compile(r'<strong class="rate_title">(.*?)<span class="title_date">')
    episode = pattern.findall(html)
    return episode

def find_date(html):
    pattern  = re.compile(r'<span class="title_date">(.*?)</span></strong>')
    date = pattern.findall(html)
    return date

def find_tvstation(html):
    pattern = re.compile(r'<span class="inline"><a nocr onclick="return goOtherCR.*?;* href=.*? target="_blank">(.*?)</a>')
    tvs = pattern.findall(html)
    return tvs[0]

def find_localtime():
    detail = time.strftime("%Y-%m-%d", time.localtime())
    return detail

def decide_day():
    # Sunday == 0
    # Monday == 1
    # Tuesday == 2
    # Wednesday == 3
    # Thursday == 4
    # Friday == 5
    # Saturday == 6
    str = time.strftime("%w", time.localtime())
    return int(str)

def write_drama_model(lctime, tvs, title, dmdate, epsd, audr, arst, defin):
    lcd = lctime.split("-")
    m = " "
    lend = len(dmdate)
    for i in range(0, lend):
        dmd = dmdate[i].split("/")
        if int(lcd[2])-1 == int(dmd[2]) and i != (lend-1):
            # current audience ratio
            thisepsd = re.findall(r'\d+\.?\d', audr[i])
            thisepsd = float(thisepsd[0])
            # last audience ratio
            lastepsd = re.findall(r'\d+\.?\d', audr[i+1])
            lastepsd = float(lastepsd[0])
            diff = str("%.1f"%(thisepsd-lastepsd))
            if thisepsd - lastepsd > 0:
                diff = "+" + diff
            if defin == 1:
                # current episode
                episode = re.findall(r'\d+',epsd[i])[0]
                m = "第" + episode + "集:" + audr[i] + "(" + diff + ") 、" + m
            else:
                m = audr[i] + "(" + diff + ") 、" + m
        elif int(lcd[2])-1 == int(dmd[2]) and i == (lend-1):
            if defin == 1:
                episode = re.findall(r'\d+', epsd[i])[0]
                m = "第" + episode + "集:" + audr[i] + "（—）、" + m
            else:
                m = audr[i] + "（—）、" + m
            break
        else:
            break
    if defin == 1: m = (tvs + " "+ title + arst + m)
    else: m = (tvs + " " + title + m)
    return m


def cable_drama(weekday):
    drama_name = [['《#请融化我#》','《#他人即地狱#》','《#我的国家#》','《#美丽爱情完美人生#》','《#黄金庭院#》'],
                  ['《#请融化我#》','《#他人即地狱#》'],
                  ['《#伟大的show#》','《#花党：朝鲜婚姻介绍所#》','《#绿豆传#》'],
                  ['《#伟大的show#》','《#花党：朝鲜婚姻介绍所#》','《#绿豆传#》'],
                  ['《#碰巧发现的一天#》','《#奔跑的调查官#》','《#青日电子李小姐#》','《#山茶花开时#》'],
                  ['《#碰巧发现的一天#》','《#奔跑的调查官#》','《#青日电子李小姐#》','《#山茶花开时#》'],
                  ['《#很便宜，千里马超市#》', '《#我的国家#》']]
    drama_kr = [['날녹여주오','타인은지옥이다','나의나라','사랑은뷰티풀인생은원더풀','황금정원'],
                ['날녹여주오','타인은지옥이다'],
                ['위대한쇼','조선혼담공작소꽃파당','녹도'],
                ['위대한쇼','조선혼담공작소꽃파당','녹도'],
                ['어쩌다발견한하루','달리는조사관','청일전자미쓰리','동백꽃필무렵'],
                ['어쩌다발견한하루','달리는조사관','청일전자미쓰리','동백꽃필무렵'],
                ['쌉니다천리마마트','나의나라']]
    drama_arst = [['（主演：#池昌旭#、#尹世雅#）','（主演：#任时完#、#李栋旭#）','（主演：#梁世宗#、#禹棹焕#、#张赫#）',
                   '（主演：#金宰英#、#吴珉锡#、#尹博#、#薛仁雅#、#赵允熙#、#金美淑#）',
                   '（主演：#韩智慧#、#李尚禹#、#吴智恩#、#李泰成#）'],
                  ['（主演：#池昌旭#、#尹世雅#）',
                   '（主演：#任时完#、#李栋旭#）'],
                  ['（主演：#宋承宪#、#李先彬#）',
                   '（主演：#金旻载#、#孔升妍#、#朴志训# ）',
                   '（主演：#金所泫#、#张东允#、#宋建熙#）'],
                  ['（主演：#宋承宪#、#李先彬#）',
                   '（主演：#金旻载#、#孔升妍#、#朴志训# ）',
                   '（主演：#金所泫#、#张东允#、#宋建熙#）'],
                  ['（主演：#金惠允#、#金路云#、#李在旭#、#郑乾柱#、#金英大#、#李泰利#、#金智仁#）',
                   '（主演：#李枖原#、#崔奎华#）',
                   '（主演：#李惠利#、#金相庆#）',
                   '（主演：#孔晓振#、#姜河那#）', ],
                  ['（主演：#金惠允#、#金路云#、#李在旭#、#郑乾柱#、#金英大#、#李泰利#、#金智仁#）',
                   '（主演：#李枖原#、#崔奎华#）',
                   '（主演：#李惠利#、#金相庆#）',
                   '（主演：#孔晓振#、#姜河那#）',],
                  ['（主演：#李东辉#、#金炳哲#、#郑惠成#、#朴浩山#、#李顺载#）',
                   '（主演：#梁世宗#、#禹棹焕#、#张赫#）']]
    lend = len(drama_name[weekday])
    lctime = find_localtime()
    print(lctime[5:7]+"月"+str(int(lctime[8:10])-1)+"日电视剧收视率")
    for i in range(0, lend):
        url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
        u = url + urllib.parse.quote(drama_kr[weekday][i])
        opener = set_ip()
        html = req_html(opener, u)
        tvs = find_tvstation(html)
        title = find_title(html)
        dmdate = find_date(html)
        epsd = find_episode(html)
        audr = find_audratio(html)
        print(write_drama_model(lctime, tvs, drama_name[weekday][i], dmdate, epsd, audr, drama_arst[weekday][i], 1)[:-2])

def cable_variety(weekday):
    variety_name = [['《#自然而然#》','《#认识的哥哥#》','《#只因工作才见面#》','《#喂狗粮的男人#》',
                     '《#惊人的星期六#》'],
                    ['《#街头大胃王2#》','《#Camping Club#》'],
                    ['《#拜托冰箱#》','《#眼神交流#》','《#冤大头的排行榜#》'],
                    ['《#最佳的一击#》','《#Idol Room#》','《#You Quiz On The Block2#》'],
                    ['《#请给我一顿饭#》','《#Rewind#》','《#星期三是音乐节目#》'],
                    ['《#西伯利亚先遣队#》','《#Queendom#》','《#Love catcher2#》','《#signhere#》'],
                    ['《柳熙烈的sketchbook》','《#begin again 3#》','《#被歌声迷住#》','《#三时三餐山村篇#》','《#新西游记外传：三时三餐-冰岛三餐#》']]
    variety_kr = [['자연스럽게','아는형님','일로만난사이','개밥주는남자','놀라운토요일도레미마켓'],
                  ['스트이트푸드파이터2','캠핑클럽'],
                  ['냉장고부탁해','아이콘택트','호구의차트'],
                  ['최고의한방','아이돌룸','유퀴즈온더블럭2'],
                  ['한끼줍쇼','리와인드','수요일은음악프로'],
                  ['시베리아신발대','퀸덤','러브캐처2','사인히어'],
                  ['유희열의스케치북','비긴어게인3','노래에반하가','삼시세끼산촌편','신서유기외전삼시세끼']]
    lend = len(variety_name[weekday])
    lctime = find_localtime()
    print(lctime)
    print(lctime[5:7] + "月" + str(int(lctime[8:10])-1) + "日综艺收视率")
    for i in range(0, lend):
        url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
        u = url + urllib.parse.quote(variety_kr[weekday][i])
        opener = set_ip()
        html = req_html(opener, u)
        tvs = find_tvstation(html)
        title = find_title(html)
        dmdate = find_date(html)
        #epsd = find_episode(html)
        # print(epsd)
        audr = find_audratio(html)
        # print(audr)
        print(write_drama_model(lctime, tvs, variety_name[weekday][i], dmdate, tvs, audr, variety_name[weekday][i], 0)[:-2])

if __name__ == '__main__' :
    weekday = decide_day()
    cable_drama(weekday)
    print()
    cable_variety(weekday)


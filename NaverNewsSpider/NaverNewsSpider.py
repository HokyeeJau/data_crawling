
import threading, time
import re
import bs4
import json
import urllib
import random
import requests
from bs4 import BeautifulSoup

def get_news():
        url = 'https://entertain.naver.com/now'
        html = build_html(url)
        #print(html)
        link = find_news_link(html)
        title = find_news_title(html)
        write_doc(link, title)

def build_html(url):
    iplist = ['45.125.32.181', '125.123.64.234', '58.22.212.39', '171.11.179.77', '125.123.126.185', '125.123.123.114',
              '58.22.213.30']
    # create an opener
    proxy_support = urllib.request.ProxyHandler({'http': iplist[random.randint(0, len(iplist) - 1)]})
    opener = urllib.request.build_opener(proxy_support)

    # create a disguise header
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36')]
    # use opener to request url
    response = opener.open(url)
    # read response and decode it
    html = response.read().decode('utf-8')
    return html

def find_news_link(req):
    pattern = re.compile('<a href="(.*?)" alt=.*? class="thumb_area"')
    result = pattern.findall(req)
    #print(result)
    return result

def find_news_title(req):
    pattern = re.compile('alt=.*? class="tit" onclick=".*?">(.*?)</a>')
    result = pattern.findall(req)
    #print(result)
    return(result)

def write_doc(link, title):
    llen = len(link)
    tlen = len(title)
    if llen == tlen:
        print('they are equal')
    i = 0
    while i < tlen:
        print(title[i])
        print(translate(title[i]))
        print('https://entertain.naver.com'+link[i])
        print()
        i+=1

def translate(content):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}
    dict = {'q':content, 'from': 'Auto', 'to': 'Auto'}
    url = 'https://aidemo.youdao.com/trans'#url 连接
    response = requests.get(url,headers=headers,params=dict)
    #print(response.text)
    result = eval(response.text)
    return result['translation'][0]

if __name__ == "__main__":
    get_news()
'''

<li>
	<a href="/now/read?oid=468&aid=0000545465" alt="" class="thumb_area" onclick="nclk(this, 'now.aimg', '', '');" >
		<img src="https://mimgnews.pstatic.net/image/origin/468/2019/08/07/545465.jpg?type=nf124_82_q90" alt="" onerror="imageError(this, 1)">
		<span class="thumb_border"></span>
	</a>
	<div class="tit_area">
		<a href="/now/read?oid=468&aid=0000545465" alt="" class="tit" onclick="nclk(this, 'now.alist', '', '');">[포토]로켓펀치, 첫 번째 미니앨범 쇼케이스</a>
		<p class="summary">신인 걸그룹 로켓펀치가 7일 서울 광진구 예스24 라이브홀에서 열린 첫 번째 미니앨범 쇼케이스에서 열정적인무대를 선보이고 있다. 왼쪽부터 수윤, 연희, 쥬리, 소희, 윤경, 다현. ‘로켓펀치’는 ‘단조로운 일상에 날</p>
		<span class="press">스포츠서울
			<em>1분전</em>
		</span>
	</div>
</li>
'''


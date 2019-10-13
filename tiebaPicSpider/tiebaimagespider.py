import requests
import urllib
import re
import os
from lxml import etree
from random import randint
class StarImageSpider:
    def __init__(self,url,name):
        self.url = url  +'&&'+ urllib.parse.urlencode({'kw':name})
        self.name = name
        self.imagenum = 1
        self.proxies = {
            'https': '58.249.55.222:9797',
            'https': '119.129.96.209:9797',
            'https': '113.121.22.247:9999',
            'https': '182.34.37.53:808'
        }
        self.UserAgengt = [
            {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'},
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
            {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        ]
    def URLupdate(self,newurl):
        self.url = newurl  +'&&'+ urllib.parse.urlencode({'kw':name})
    def HTMLDownloading(self,selectedurl):
        length = len(self.UserAgengt)
        response = requests.get(url=selectedurl,headers=self.UserAgengt[randint(0,length-1)])
        return response.text
    def ImageDownloading(self,selectedurl):
        if not os.path.isdir('images'):
            os.mkdir('images')
        length = len(self.UserAgengt)
        response = requests.get(url=selectedurl, headers=self.UserAgengt[randint(0, length - 1)])
        return response.content
    def InteprteImageUrl(self,html,pattern):
        urllist = pattern.findall(html)
        return urllist

    def WriteFile(self,filename,html):
        f = open(filename+'.html','w',encoding='utf-8')
        f.write(html)
        f.close()
    def SaveImage(self,image,n):
        print('loading......'+self.name + str(n))
        f = open('./images/'+self.name + str(n) + '.png','wb')
        f.write(image)
        f.close()


if __name__ == '__main__':
    weburl = 'https://tieba.baidu.com/f?ie=utf-8&pn='
    name = input('name:')
    begin = int(input('begin page:'))
    end = int(input('ending page:'))
    num = 1
    for i in range(begin,end+1):
        pn = (i-1)*50
        weburl +=str(pn)
        starimagespider = StarImageSpider(weburl,name)
        html = starimagespider.HTMLDownloading(starimagespider.url)
        penter = re.compile(r'href="/p/\d+"')
        #获得各个评论url
        newurllist = starimagespider.InteprteImageUrl(html,penter)

        p = re.compile(r'/p/\d+')#去掉href=
        pfindImage = re.compile('https?://imgsrc.baidu.com/.*?\.[jpgn]{3}')#图片url匹配
        for i in newurllist:
            lastname = p.findall(i)[0]
            newurl = 'https://tieba.baidu.com' + lastname#拼接得到url

            html = starimagespider.HTMLDownloading(newurl)
            Imagelist = pfindImage.findall(html)
            length = len(Imagelist)

            for i in range(length):
                pic = starimagespider.ImageDownloading(Imagelist[i])
                starimagespider.SaveImage(image=pic,n=num)
                num +=1





    # p = re.compile(r'src="https?://.*.jpg"')
    # pnext = re.compile(r'"href=/p/\w+"')
    # purl = re.compile(r'https?://.+')


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
            {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:69.0) Gecko/20100101 Firefox/69.0'}
        ]
    # def downloadVideo(self, url):
    #
    #     video =
    #     f = open('khc.mp4', 'ab')
    #     f.write(video.content)
    #     f.close()
    def URLupdate(self, url):
        self.url = url + '&&' + urllib.parse.urlencode({'kw': name})

    def HTMLDownloading(self, selectedurl):
        length = len(self.UserAgengt)
        response = requests.get(url = selectedurl, headers = self.UserAgengt[randint(0, length-1)])
        return response.text

    def ImageDownloading(self, selectedurl):
        if not os.path.isdir('images'):
            os.mkdir('images')
        length = len(self.UserAgengt)
        response = requests.get(url = selectedurl, headers = self.UserAgengt[randint(0, length - 1)])
        return response.content

    def InteprteImageUrl(self,html, pattern):
        urllist = pattern.findall(html)
        return urllist

    def SaveImage(self, image, n):
        print('loading......' + self.name + str(n))
        f = open('./images/' + self.name + str(n) + '.png', 'wb')
        f.write(image)
        f.close()

    def WriteFile(self,filename,html):
        f = open(filename+'.html','w',encoding='utf-8')
        f.write(html)
        f.close()




if __name__ == '__main__':
    url = 'https://tieba.baidu.com/f?ie=utf-8&pn='
    name = input('name:')
    beginPage = int(input('begin page:'))
    endPage = int(input('ending page:'))
    num = 1
    for i in range(beginPage, endPage + 1):
        #贴吧链接尾部更改
        pn = (i-1)*50
        url += str(pn)
        #建立对象与有关键字的链接
        starSpider = StarImageSpider(url, name)
        #返回response.text
        html = starSpider.HTMLDownloading(starSpider.url)
        #建立寻找的图片链接格式
        penter = re.compile(r'href="/p/\d+"')
        #获取所有符合格式的链接列表
        newUrlList = starSpider.InteprteImageUrl(html, penter)
        #对列表进行精化（去href）
        p = re.compile(r'/p/\d+')
        #百度图片的链接格式
        findImage = re.compile('https?://imgsrc.baidu.com/.*?\.[jpgn]{3}')#图片url匹配
        #百度视频格式
        pattern = re.compile("http://tb-video.bdstatic.com/tieba-smallvideo-transcode/.*?.mp4")
        newVideoList = starSpider.InteprteImageUrl(html, pattern)
        # for i in newVideoList:
        #     length = len(newVideoList)

        for i in newUrlList:#遍历图片链接列表
            last = p.findall(i)[0]
            newUrl = 'https://tieba.baidu.com' + last#拼接得到url
            #传输HTML字节流
            html = starSpider.HTMLDownloading(newUrl)
            #
            Imagelist = findImage.findall(html)
            length = len(Imagelist)

            for i in range(length):
                pic = starSpider.ImageDownloading(Imagelist[i])
                starSpider.SaveImage(image = pic, n = num)
                num +=1

    # p = re.compile(r'src="https?://.*.jpg"')
    # pnext = re.compile(r'"href=/p/\w+"')
    # purl = re.compile(r'https?://.+')


# url = 'https://www.youtube.com/935eab15-5dc4-9c4f-9d40-d3caca6c0e5b'
# userAgent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
# proxi = {'https': '58.249.55.222:9797'}
# response = requests.get(url=url, headers=userAgent)
# req = response.content
# f = open('第九集预告.mp4', 'wb')
# f.write(req)
# f.close()
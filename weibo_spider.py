# -*-coding:utf8-*-


# import time
import re
# import string
#
import urllib
import urllib2
from bs4 import BeautifulSoup
#
# from io import StringIO

import os

import requests
from lxml import etree

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
import cookielib
#第一步：得到一个cookie实例对象来保存Cookie内容
cookie=cookielib.CookieJar()
#第二步：利用urllib2库的HTTPCookieProcessor对象
hander=urllib2.HTTPCookieProcessor(cookie)

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

#第三步：得到一个opener
opener=urllib2.build_opener(hander)
request = urllib2.Request("http://weibo.cn/", headers=headers)
print opener.open(request).read().decode('utf-8')
'''

if len(sys.argv) >= 2:
    user_id = int(sys.argv[1])
    page_limit = int(sys.argv[2])
else:
    user_id = int(raw_input(u"请输入user_id: "))

agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
cookie = {
    'Cookie': '_T_WM=47a585d1a07b2baa0f45fe641f1dfe7e; SUB=_2A2578QyDDeRxGedJ41IT9SbJzjuIHXVZHZTLrDV6PUJbrdBeLU3BkW1LHeuYt75k9b4KUO3dLz8FNu19qc28og..; SUHB=08J6pvl74_fGmw; SSOLoginState=1458928851; gsid_CTandWM=4uaTCpOz5Kd6kMhsJ7B997t7Q8Z; H5_INDEX=3; H5_INDEX_TITLE=%E9%82%A3%E5%8F%AA%E7%8C%B4%E5%AD%90_%E8%91%B5; M_WEIBOCN_PARAMS=featurecode%3D20000180%26oid%3D3957083668106947%26luicode%3D20000061%26lfid%3D3957083668106947'}

retcode = '&retcode=6102'
# url = 'http://weibo.cn/u/%d?filter=1&page=1%s'%(user_id,retcode)
# html = requests.get(url, cookies = cookie, headers = agent).content


# p = re.compile('location\.replace\(\"(.*?)\"\)')
# login_url = p.search(html).group(1)
#retcode = login_url[login_url.find('page=1')+len('page=1'):]

#rehtml = requests.get(login_url, cookies = cookie).content

#selector = etree.HTML(html)

'''
data = {
    'entities_only':'true'
    'page':'1'
}
html_post = requests.post(url, data=data)
title = re.findall('XXXX(.*?)XXX', html.txt, re.S)
for each in title:
    print each
'''

result = ""
urllist_set = set()
word_count = 1
image_count = 1
pageNum = -1
page = 1
print u'爬虫准备就绪...'

while True:

    #  time.sleep(20)

    '''
      opener = urllib2.build_opener()
      opener.addheaders.append(('Cookie', 'SUB=_2A257942-DeRxGedJ41IT9SbJzjuIHXVZGxP2rDV6PUJbstBeLVfykW1LHesNpN9U0sKFDn-EPtIqyOIkhVYCWg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWO1IrMp.oGq_0OczG__xGW5JpX5o2p; SUHB=0LcTc9Y4LU3b8c; SSOLoginState=1458830830; _T_WM=47a585d1a07b2baa0f45fe641f1dfe7e; gsid_CTandWM=4uVzCpOz5GmWHWwGdqVif7t7Q8Z; H5_INDEX=3; H5_INDEX_TITLE=%E9%82%A3%E5%8F%AA%E7%8C%B4%E5%AD%90_%E8%91%B5; M_WEIBOCN_PARAMS=uicode%3D20000174'))
      xx = opener.open(url)
    '''

    url = 'http://weibo.cn/u/%d?page=%d' % (user_id, page)
    lxml = requests.get(url, cookies=cookie, headers=agent).content
    selector = etree.HTML(lxml)

    if pageNum == -1:
        pageNum = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

    content = selector.xpath('//div[@class="c"]')

    for each in content:
        text = each.xpath('div/span[@class="ctt"]')
        if len(text) == 1:
            text = text[0].xpath('string(.)')
        else:
            continue
        msg_time = each.xpath('div/span[@class="ct"]/text()')[0]
        text = "%d: %s: %s\n\n" % (word_count, msg_time, text)
        result = result + text
        word_count += 1

    # get pic
    soup = BeautifulSoup(lxml, "lxml")
    urllist = soup.find_all('a', href=re.compile(r'^http://weibo.cn/mblog/oripic', re.I))
    first = 0
    for imgurl in urllist:
        urllist_set.add(requests.get(imgurl['href'], cookies=cookie, headers=agent).url)
        image_count += 1

    print u'page: %d, word_count: %d, image_count: %d' % (page, word_count, image_count)
    page += 1
    if page > pageNum or page > page_limit:
        break



if os.path.exists("weibo") is False:
    os.mkdir("weibo")

fo = open("weibo/%s" % user_id, "wb")
fo.write(result)
word_path = os.path.abspath(fo.name)
print u'文字微博爬取完毕'
fo.close()

link = ""
fo2 = open("weibo/%s_imageurls" % user_id, "wb")
for eachlink in urllist_set:
    link = link + eachlink + "\n"
fo2.write(link)
print u'图片链接爬取完毕'
fo2.close()

if not urllist_set:
    print u'该页面中不存在图片'
else:
    # os.getcwd()
    #下载图片,保存在当前目录的pythonimg文件夹下
    image_path = 'weibo/%s_image/' % user_id
    if os.path.exists(image_path) is False:
        os.makedirs(image_path)
    x = 1
    for imgurl in urllist_set:
        temp = image_path + '/%s.jpg' % x
        print u'正在下载第%s张图片' % x
        try:
            urllib.urlretrieve(urllib2.urlopen(imgurl).geturl(), temp)
        except:
            print u"该图片下载失败:%s" % imgurl
        x += 1

print u'原创微博爬取完毕，共%d条，保存路径%s' % (word_count - 1, word_path)
print u'微博图片爬取完毕，共%d张，保存路径%s' % (image_count - 1, image_path)



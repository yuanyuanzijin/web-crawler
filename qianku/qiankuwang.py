import urllib
import requests
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import socket
import os
socket.setdefaulttimeout(5.0)

foldername = input('请指定图片下载保存名称（英文）：')
if not os.path.exists('download/' + foldername):  # 新建文件夹
    os.mkdir('download/' + foldername)

weburl = input('请粘贴千库网网址(例如：http://588ku.com/sucai/0-default-0-0-18030-)')
    
pagenum = int(input('请输入要爬取的页数：'))
x = 1

for page in range(pagenum):
    y = page+1
    req = urllib.request.urlopen(weburl + str(y))
    soup = BeautifulSoup(req.read(),'html.parser')
    strawberries = soup.select('.picture-list img')
    for i in strawberries:
        img_url = i['data-original']
        try:
            filepath = os.path.join('download', foldername, foldername+'%s.jpg' % x)
            urllib.request.urlretrieve(img_url, filepath)
            print("下载完成第%d张图片:%s" % (x,img_url))
            x += 1
        except Exception as e:
            print("下载图片失败:%s" % (img_url))
            print(e)
    

    print('第%d页下载完毕' % int(y))
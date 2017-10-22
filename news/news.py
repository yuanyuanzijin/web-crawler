import spider

cookie = spider.Cookie()
back = spider.open('http://www.baidu.com')

print(cookie.get('BAIDUID'))

import spider as zspider

cj = zspider.open_cookie()
back = zspider.get('http://www.baidu.com')
cookies = zspider.read_cookie(cj)
print(cookies)

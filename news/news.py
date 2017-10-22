import spider as zspider

back = zspider.get('https://baidu.com', proxy='localhost:1081')
print(back)

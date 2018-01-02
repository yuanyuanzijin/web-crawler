import requests
from bs4 import BeautifulSoup
import execjs

print('\n********** 欢迎使用大连理工大学个人信息综合管理系统 **********')

username = ''
password = ''

s = requests.Session()

def get_key(username, password, ticket):  
    f = open("./des.js", 'r', encoding='UTF-8')  
    line = f.readline()  
    htmlstr = ''  
    while line:  
        htmlstr = htmlstr + line  
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    rsa = ctx.call('strEnc',username+password+ticket, '1', '2', '3')
    return rsa  

url = "https://sso.dlut.edu.cn/cas/login?service=http%3A%2F%2Fportal.dlut.edu.cn%2Ftp%2F"
req = s.get(url, allow_redirects=False)
soup = BeautifulSoup(req.text, 'html.parser')

ticket = soup.select('#lt')[0]['value']
execution = soup.select('input')[4]['value']
rsa = get_key(username, password, ticket)
jsessionid = req.cookies['JSESSIONID']

headers = {
    'Origin': 'https://sso.dlut.edu.cn',
    'Host': 'sso.dlut.edu.cn',
    'Referer': 'https://sso.dlut.edu.cn/cas/login?service=http%3A%2F%2Fportal.dlut.edu.cn%2Ftp%2F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
data = {
    'rsa': rsa,
    'ul': len(username),
    'pl': len(password),
    'lt': ticket,
    'execution': execution,
    '_eventId': 'submit'
}
req = s.post(url, data=data, headers=headers, allow_redirects=False)
soup = BeautifulSoup(req.text, 'html.parser')
newaddr = soup.select('a')[0]['href']
print(newaddr)

req = s.get(newaddr, allow_redirects=True)

import requests
from bs4 import BeautifulSoup
import execjs
import getpass

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

print('\n********** 欢迎使用大连理工大学研究生成绩查询系统 **********')

while 1:

    while 1:
        username = input('请输入学号：')
        if username:
            break
    while 1:
        password = getpass.getpass('请输入密码：')
        if password:
            break

    print('正在登录...')

    s = requests.Session()

    url = "https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx"
    req = s.get(url, allow_redirects=False)
    soup = BeautifulSoup(req.text, 'html.parser')

    ticket = soup.select('#lt')[0]['value']
    execution = soup.select('input')[4]['value']
    rsa = get_key(username, password, ticket)
    jsessionid = req.cookies['JSESSIONID']

    url2 = "https://sso.dlut.edu.cn/cas/login;jsessionid=%s?service=http://202.118.65.123/gmis/LoginCAS.aspx" % jsessionid

    headers = {
        'Origin': 'https://sso.dlut.edu.cn',
        'Host': 'sso.dlut.edu.cn',
        'Referer': 'https://sso.dlut.edu.cn/cas/login?service=http://202.118.65.123/gmis/LoginCAS.aspx',
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

    req = s.post(url2, data=data, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(req.text, 'html.parser')
    newaddr = soup.select('a')[0]['href']
    if newaddr.find("javascript") < 0:
        print("SSO登录成功！正在查询成绩...")
        break
    else:
        print("登录失败，请重试！")

req = s.get(newaddr, allow_redirects=True)
req = s.get('http://202.118.65.123/pyxx/grgl/xskccjcx.aspx?xh=%s' % username)
soup = BeautifulSoup(req.text, 'html.parser')

bx_scores = soup.select('#MainWork_dgData tr')[1:]
print('\n共找到%d条必修课成绩' % len(bx_scores))
for score in bx_scores:
    soup1 = BeautifulSoup(str(score), 'html.parser')
    name = soup1.select('td')[0].text
    value = soup1.select('span')[0].text
    print(name, value)

xx_scores = soup.select('#MainWork_Datagrid1 tr')[1:]
print('\n共找到%d条选修课成绩' % len(xx_scores))
for score in xx_scores:
    soup2 = BeautifulSoup(str(score), 'html.parser')
    name = soup2.select('td')[0].text
    value = soup2.select('span')[0].text
    print(name, value)

input('\n按Enter键退出...')
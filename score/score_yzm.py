import requests
import getpass
import os
from bs4 import BeautifulSoup

print('\n********** 欢迎使用大连理工大学研究生成绩查询系统 **********')
s = requests.Session()
url_home = "http://202.118.65.123/pyxx/login.aspx"
req = s.get(url_home)
soup = BeautifulSoup(req.text, "html.parser")
VIEWSTATE = soup.select("#__VIEWSTATE")[0]['value']
VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
while 1:
    ir = s.get('http://202.118.65.123/pyxx/PageTemplate/NsoftPage/yzm/createyzm.aspx')
    if ir.status_code == 200:
        open('code.jpg', 'wb').write(ir.content)
    while 1:
        username = input('请输入学号：')
        if username:
            break
    while 1:
        password = getpass.getpass('请输入密码：')
        if password:
            break
    os.system('code.jpg')
    while 1:
        code = input('请输入验证码：')
        if code:
            break

    headers = {
        'Origin': 'http://202.118.65.123',
        'Referer': 'http://202.118.65.123/pyxx/login.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        'ctl00$txtusername': username,
        'ctl00$txtpassword': password,
        'ctl00$txtyzm': code,
        'ctl00$ImageButton1.x': 0,
        'ctl00$ImageButton1.y': 0
    }
    req = s.post('http://202.118.65.123/pyxx/login.aspx', data=data, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    f = soup.select('frameset')
    if len(f) > 0:
        print('登录成功！')
        break
    else:
        print('登录失败，请重试！')

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
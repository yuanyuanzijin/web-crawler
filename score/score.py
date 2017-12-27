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
ir = s.get('http://202.118.65.123/pyxx/PageTemplate/NsoftPage/yzm/createyzm.aspx')
if ir.status_code == 200:
    open('code.jpg', 'wb').write(ir.content)
username = input('请输入学号：')
password = getpass.getpass('请输入密码：')
os.system('code.jpg')
code = input('请输入验证码：')

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
else:
    print('登录失败，请重试！')
    exit()

req = s.get('http://202.118.65.123/pyxx/grgl/xskccjcx.aspx?xh=%s' % username)
soup = BeautifulSoup(req.text, 'html.parser')
scores = soup.select('#MainWork_dgData tr')[1:]
print('\n共找到%d条成绩：' % len(scores))
for score in scores:
    soup = BeautifulSoup(str(score), 'html.parser')
    name = soup.select('td')[0].text
    value = soup.select('span')[0].text
    print(name, value)

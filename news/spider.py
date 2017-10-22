import urllib
import urllib.request

def get(url, charset=None, proxy=None):
    if proxy:
        opener = open_proxy(proxy)
        response = opener.open(url)
    else:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

    if not charset:
        charset = auto_charset(response)
    return response.read().decode(charset)

def post(url, data=None, headers=None, charset=None, proxy=None):
    form_data = urllib.parse.urlencode(data).encode('utf-8')
    if proxy:
        opener = open_proxy(proxy)
        response = opener.open(url)
    else:
        request = urllib.request.Request(url, data=form_data, headers=headers)
        response = urllib.request.urlopen(request)

    if not charset:
        charset = auto_charset(response)
    return response.read().decode(charset)

def open_proxy(proxy):
    print('开启代理访问 ' + proxy)
    set_proxy = urllib.request.ProxyHandler({'socks5': proxy})  # 设置proxy
    opener = urllib.request.build_opener(set_proxy)  # 挂载opener
    urllib.request.install_opener(opener)  # 安装opener
    return opener

def auto_charset(response):
    charset = response.info().get_param('charset')
    if not charset:
        charset = 'utf-8'
    return charset
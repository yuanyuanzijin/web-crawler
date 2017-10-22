import urllib
import urllib.request
import http.cookiejar

def get(url, charset=None):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)

    if charset:
        print('您已指定编码：' + charset)
    else:
        charset = judge_charset(response)

    content = response.read()
    response = try_decode(content, charset)
    return response

def post(url, data=None, headers=None, charset=None):
    form_data = urlencode(data)
    request = urllib.request.Request(url, data=form_data, headers=headers)
    response = urllib.request.urlopen(request)

    if charset:
        print('您已指定编码：' + charset)
    else:
        charset = judge_charset(response)

    content = response.read()
    response = try_decode(content, charset)
    return response

def urlencode(data):
    form_data = urllib.parse.urlencode(data).encode('utf-8')
    return form_data

def open_proxy(proxy):
    print('通过http代理访问 ' + proxy)
    set_proxy = urllib.request.ProxyHandler({'http': proxy})  # 设置proxy
    opener = urllib.request.build_opener(set_proxy)  # 挂载opener
    urllib.request.install_opener(opener)  # 安装opener
    return

def open_cookie():
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    return cookie

def read_cookie(cj):
    cookies = []
    for item in cj:
        clist = {
            'name': item.name,
            'value': item.value
        }
        cookies.append(clist)
    return cookies

def judge_charset(response):
    charset = response.info().get_param('charset')
    if charset:
        print('您未指定编码，自动检测结果：' + charset)
    else:
        charset = 'utf-8'
        print('您未指定编码，自动检测失败，尝试使用utf-8解码')
    return charset

def try_decode(content, charset):
    try:
        response = content.decode(charset)
    except Exception as e:
        response = content
        print('编码解析失败，为您返回源码')
    return response

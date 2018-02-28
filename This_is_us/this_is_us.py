# -*- coding: utf-8 -*-
import re
from urllib import request
from http import cookiejar
from urllib import parse
from bs4 import BeautifulSoup
import time
import socket


# 用于生成短评页面网址的函数
def MakeUrl(start):
    """make the next page's url"""
    url = 'https://movie.douban.com/subject/26794215/comments?start=' + str(start) + '&limit=20&sort=new_score&status=P'
    return url


# 登录页面信息
main_url = 'https://accounts.douban.com/login?source=movie'
formdata = {
    "form_email": "你的账号",
    "form_password": "你的密码",
    "source": "movie",
    "redir": "https://movie.douban.com/subject/26794215/",
    "login": "登录"
}
user_agent = r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}

# 保存cookies便于后续页面的保持登陆
cookie = cookiejar.CookieJar()
cookie_support = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(cookie_support)

# 编码信息，生成请求，打开页面获取内容
logingpostdata = parse.urlencode(formdata).encode('utf-8')
req_ligin = request.Request(url=main_url, data=logingpostdata, headers=headers)
response_login = opener.open(req_ligin).read().decode('utf-8')

# 获取验证码图片地址
try:
    soup = BeautifulSoup(response_login, "html.parser")
    captchaAddr = soup.find('img', id='captcha_image')['src']

    # 匹配验证码id
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID, response_login)

    # 下载验证码图片
    request.urlretrieve(captchaAddr, "captcha.jpg")

    # 输入验证码并加入提交信息中，重新编码提交获得页面内容
    captcha = input('please input the captcha:')
    formdata['captcha-solution'] = captcha
    formdata['captcha-id'] = captchaID[0]
    logingpostdata = parse.urlencode(formdata).encode('utf-8')
    req_ligin = request.Request(url=main_url, data=logingpostdata, headers=headers)
    response_login = opener.open(req_ligin).read().decode('utf-8')

finally:
    # 获得页面评论文字
    soup = BeautifulSoup(response_login, "html.parser")
    totalnum = soup.select("div.mod-hd h2 span a")[0].get_text()[3:-2]

    # 计算出页数和最后一页的评论数
    pagenum = int(totalnum) // 20
    commentnum = int(totalnum) % 20
    print(pagenum, commentnum)

    # 设置等待时间，避免爬取太快
    # 用于在超时的时候抛出异常，便于捕获重连

    timeout = 3
    socket.setdefaulttimeout(timeout)

    # 追加写文件的方式打开文件
    with open('This is us的短评.txt', 'w+', encoding='utf-8') as file:
        # 循环爬取内容
        for item in range(pagenum):
            print('第' + str(item) + '页')
            start = item * 20
            url = MakeUrl(start)

            # 超时重连
            state = False
            while not state:
                try:
                    html = opener.open(url).read().decode('utf-8')
                    state = True
                except socket.timeout:
                    state = False
                    print('超时重连..')

            # 获得评论内容
            soup = BeautifulSoup(html, "html.parser")
            comments = soup.select("div.comment > p")
            for text in comments:
                file.write(text.get_text().split()[0] + '\n')
                print('获得短评..')
                limit_num = 0
                if item == pagenum - 1:
                    limit_num = + 1
                    if limit_num == commentnum:
                        break
            time.sleep(3)

    print('采集写入完毕')

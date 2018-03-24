# -*- coding:utf-8 -*-
import requests
import re


def get_one_page(url):
    headers = {
        "Origin": "https://www.instagram.com/",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/65.0.3325.181 Safari/537.36",
        "Host": "www.instagram.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "zh-CN,zh;q=0.8",
        "X-Instragram-AJAX": "1",
        "X-Requested-With": "XMLHttpRequest",
        "Upgrade-Insecure-Requests": "1",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response.encoding = 'gzip'
        return response.text
    else:
        return None


def parse_one_page(html):
    results = re.search(r'<meta property="og:description" content="(.*?) 位.*?关注 (.*?) 人.*? (.*?) 篇', html)
    if results:
        watches = results.group(1)
        watching = results.group(2)
        posts = re.sub('\D', '', results.group(3))
        return [watches, watching, posts]
    else:
        return None


def main():
    user = "rossbutler"
    url = "https://www.instagram.com/{0}/".format(user)
    html = get_one_page(url)
    results = parse_one_page(html)
    if results:
        print('用户：', user)
        print('关注人数：', results[0])
        print('正在关注：{0}人'.format(results[1]))
        print('帖子数：', results[2])
    else:
        print('抓取失败。')


if __name__ == '__main__':
    main()

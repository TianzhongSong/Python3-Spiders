# -*- coding:utf-8 -*-
from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'your cookie',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
}
keyword = 'python'
proxy = None
max_count = 5


def get_proxy():
    try:
        r = requests.get('http://127.0.0.1:5000/get')
        proxy = BeautifulSoup(r.text, "lxml").get_text()
        return proxy
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling:', url)
    print('Trying count:', count)
    global proxy
    if count >= max_count:
        print('Tried too many times')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using proxy:', proxy)
                return get_html(url)
            else:
                print('Failed to get proxy')
                return None
    except ConnectionError as e:
        print('Error Occured:', e.args)
        count += 1
        proxy = get_proxy()
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print('Current page:', page)
        if html:
            articles_urls = parse_index(html)
            for articles_url in articles_urls:
                print(articles_url)


if __name__ == "__main__":
    main()

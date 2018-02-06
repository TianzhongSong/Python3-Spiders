# -*- coding: utf-8 -*-
import json
from time import sleep
import re
import requests
from bs4 import BeautifulSoup
from requests import RequestException


def save_to_file(content):
    with open('result.txt','a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii= False) + '\n')
        f.close()


def get_proxy():
    r = requests.get('http://127.0.0.1:5000/get')
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy


def get_comment_number(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                        (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            doc = BeautifulSoup(response.text, 'lxml')
            total = doc.select('.is-active')[0].span.string
            total = int(re.search('(\d+)', total).group(1))
            return total
        else:
            return None
    except RequestException:
        return None


def get_one_page(url, proxy):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                        (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"}
        proxies = {'http': proxy}
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('.comment-item .comment')
    for item in items:
        comment = item.p.string
        if comment:
            save_to_file(comment.strip())


def main(start, proxy):
    prefix = 'https://movie.douban.com/subject/26794215/comments?start='
    url = prefix + str(start*20) + '&limit=20&sort=new_score&status=P&percent_type='
    html = get_one_page(url, proxy)
    parse_one_page(html)


if __name__ == "__main__":
    url = 'https://movie.douban.com/subject/26794215/comments?status=P'
    total = get_comment_number(url)
    print('total comment number is:', total)
    proxy = get_proxy()
    for i in range(total//20):
        if i % 10 == 0:
            proxy = get_proxy()
            print('current ip:', proxy)
        sleep(1)
        print('Current page:', i)
        main(i, proxy)

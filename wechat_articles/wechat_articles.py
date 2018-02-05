# -*- coding:utf-8 -*-
from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'CXID=02ADC062D77AE47FC443E8FB59E9AE73; \
    ad=Oyllllllll2zb$SNlllllVImIV1lllllt9VD1lllll9lllll4ylll5@@@@@@@@@@; \
    SUID=D07C41705B68860A5A6EA45D000B354F; SUV=00CE0B5C70417CCA5A72BCCA94D02067; \
    IPLOC=CN3100; SNUID=72FF8AE2F8FD9CBD7FB0303BF982B1F8; sct=2; \
    ppinf=5|1517621574|1518831174|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbm\
    FtZToyNzolRTUlQUUlOEIlRTUlQTQlQTklRTQlQjglQUR8Y3J0OjEwOjE1MTc2MjE1NzR8cmVmbmljaz\
    oyNzolRTUlQUUlOEIlRTUlQTQlQTklRTQlQjglQUR8dXNlcmlkOjQ0Om85dDJsdUp2YnFqVEoyYUV5bVhjcmt\
    JZFlfUmdAd2VpeGluLnNvaHUuY29tfA; pprdig=tOyRk2QPRlGEW6ufWTT06fRyq0QWvrIR4_6VJKSiNuQqf\
    voWAX9bExd6rNbET6t9y7uEIYCkqHRfJ4wcKewwZSkLqq2uHMRu3PaKe5jNb-PCUgx09bUF_UG0ARlM2yb7tPB\
    XjWp10BpAEP_fsNyWyJqtDNgnPhq7VGGV5OFqTEs; sgid=21-33348115-AVp1EUaQch2ocdoZVxkfJBg; ppmd\
    ig=15176215750000005c9f33dcdbf69310ed560b835b5eaee3',
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

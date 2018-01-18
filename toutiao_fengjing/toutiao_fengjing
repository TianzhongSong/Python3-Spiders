# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
from bs4 import  BeautifulSoup
from time import sleep
from hashlib import md5
from multiprocessing import Pool
import re
import json
import os
import pymongo


client = pymongo.MongoClient('localhost', connect=False)
db = client['toutiao']


def get_page_index(offset):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': '风景',
        'autoload': 'ture',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页失败。')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错。')
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('gallery:\sJSON.parse..(.*?)..,\n', re.S)
    results = re.search(images_pattern, html)

    if results:
        results = results.group(1).replace('\\', '')
        data = json.loads(results)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                sleep(1)
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(content):
    if db['toutiao'].insert(content):
        print('存储到mongodb成功。')
        return True
    return False


def download_image(url):
    print('正在下载：', url)
    response = requests.get(url)
    try:
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错。')
        return None


def save_image(content):
    if not os.path.exists('images/'):
        os.mkdir('images/')
    file_path = 'images/{0}.{1}'.format(md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset=offset)
    for url in parse_page_index(html):
        if url:
            detail_html = get_page_detail(url)
            sleep(1)
            if detail_html:
                result = parse_page_detail(detail_html, url)
                if result:
                    save_to_mongo(result)


if __name__ == "__main__":
    groups = [i*20 for i in range(1, 21)]
    pool = Pool()
    pool.map(main, groups)

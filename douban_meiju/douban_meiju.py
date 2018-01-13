# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from time import sleep
import csv


def write_to_file(content):
    with open('douban_meiju.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(content)
        csvfile.close()


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('.item')
    for item in items:
        try:
            score = item.find(class_="rating_nums").string
        except:
            score = 0.0
        yield [
            item.a['title'],
            score,
            item.find(class_="star clearfix").find(class_="pl").string
        ]


if __name__ == "__main__":
    prefix = u'https://movie.douban.com/tag/美剧?start='
    results = []
    for i in range(144):
        sleep(1)
        print(i)
        url = prefix + str(i*20) + '&type=T'
        html = get_one_page(url)
        for item in parse_one_page(html):
            results.append(item)
    write_to_file(results)

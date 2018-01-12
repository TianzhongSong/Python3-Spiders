# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from time import sleep
import csv


def write_to_file(content):
    with open('result_bs4.csv', 'w') as csvfile:
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
    soup.prettify()
    info = []
    prefix = 'http://sh.lianjia.com'
    for items in soup.select('.info-panel'):
        for item in items.select('h2'):
            for sub_item in item.select('a'):
                info.append(sub_item['href'])
                info.append(sub_item['title'])

        for item in items.select('.col-1'):
            for sub_item in item.select('.where'):
                for span in sub_item.select('span'):
                    info.append(span.get_text())

            for sub_item in item.select('.other'):
                for a in sub_item.select('a'):
                    info.append(a.get_text())
            for sub_item in item.select('.chanquan'):
                for span in sub_item.select('span'):
                    info.append(span.get_text())

        for item in items.select('.col-3'):
            for span in item.select('span'):
                info.append(span.get_text())
            for div in item.select('.price-pre'):
                info.append(div.get_text())

        for item in items.select('.col-2'):
            for span in item.select('span'):
                info.append(span.get_text())
        info_temp = list(set(info))
        info_temp.sort(key=info.index)
        info = []
        info_temp[0] = prefix + info_temp[0]
        info_temp[3] = info_temp[3].split('\xa0\xa0')[0]
        info_temp[4] = info_temp[4].split('\xa0\xa0')[0]
        info_temp[11] = info_temp[11].split('\n')[0]
        del info_temp[7]
        yield info_temp


def main(page, results):
    url = 'http://sh.lianjia.com/zufang/d' + str(page)
    html = get_one_page(url)
    for item in parse_one_page(html):
        results.append(item)


if __name__ == '__main__':
    results = []
    for i in range(100):
        sleep(1)
        main(i+1, results)
    write_to_file(results)

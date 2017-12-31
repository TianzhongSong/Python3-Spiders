# -*- coding:utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import json
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('result.txt','a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii= False) + '\n')
        f.close()


def analysis(content):
    years = {}
    area = {}
    actors = {}
    for info in content:
        if info['time'].split('-')[0] not in years:
            years[info['time'].split('-')[0]] = 1
        else:
            years[info['time'].split('-')[0]] += 1

        if len(info['time'].split('(')) > 1:
            if (info['time'].split('(')[-1]).split(')')[0] not in area:
                area[(info['time'].split('(')[-1]).split(')')[0]] = 1
            else:
                area[(info['time'].split('(')[-1]).split(')')[0]] += 1
        else:
            if u'其他' not in area:
                area[u'其他'] = 1
            else:
                area[u'其他'] += 1
        # print(info['actor'])
        names = info['actor'].split(',')
        for name in names:
            if name not in actors:
                actors[name] = 1
            else:
                actors[name] += 1
    years = sorted(years.items(), key=lambda item:item[0])
    year = []
    count = []
    for item in years:
        year.append(item[0])
        count.append(item[1])
    a = [i for i in range(1, len(year)+1)]
    plt.bar(a, count, 0.4, color="red")
    xlocations = np.array(range(1, len(year)+1))
    plt.xticks(xlocations, year, rotation=60)
    plt.ylabel(u"电影数量")
    plt.title(u"Top100电影年份分布")
    plt.savefig(u"Top100电影年份分布.jpg", dpi=300)
    plt.close()

    areas = sorted(area.items(), key=lambda item: item[1])
    area = []
    count = []
    for item in areas:
        area.append(item[0])
        count.append(item[1])
    a = [i for i in range(1, len(area) + 1)]
    plt.bar(a, count, 0.4, color="blue")
    xlocations = np.array(range(1, len(area) + 1))
    plt.xticks(xlocations, area, rotation=30)
    plt.ylabel(u"电影数量")
    plt.title(u"Top100电影地区分布")
    plt.savefig(u"Top100电影地区分布.jpg", dpi=300)
    plt.close()

    actors = sorted(actors.items(), key=lambda item: item[1], reverse=True)
    actor = []
    count = []
    a = [i for i in range(1, 11)]
    for i in range(10):
        actor.append(actors[i][0])
        count.append(actors[i][1])
    plt.bar(a, count, 0.4, color="green")
    xlocations = np.array(range(1, len(actor)+1))
    plt.xticks(xlocations, actor, rotation=15)
    plt.ylabel(u"参演电影数量")
    plt.title(u"Top100电影年份分布")
    plt.savefig(u"Top100电影中top10影星.jpg", dpi=300)
    plt.close()

def main(offset, results):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        results.append(item)


if __name__ == '__main__':
    results = []
    for i in range(10):
        sleep(1)
        main(i*10, results)
    analysis(results)

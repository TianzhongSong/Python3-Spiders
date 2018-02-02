### 豆瓣美剧评分信息

#### douban_meiju.py
只抓取了豆瓣上所有美剧的剧名，评分及总评分人数。

#### douban_meiju_v2.py
抓取豆瓣上所有美剧的详细信息，先获取搜索页上所有美剧的url，再进入每部美剧的详细页获取信息，包括“导演”、“编剧”、“主演”等等。但是没有反反爬虫措施，目前程序还不能直接爬取。

#### douabn_meiju_v3.py
抓取内容同v2，使用代理处理反爬问题。

代理池使用的是[Proxy_Pool](https://github.com/TianzhongSong/Python3-Spiders/tree/master/ProxyPool) 

先在终端运行Proxy_Pool中的run.py

python run.py

确保代理池维护程序正常运作，然后再运行douban_meiju_v3.py

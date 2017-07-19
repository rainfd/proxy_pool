# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""
import time
import requests
import random

import utils

HEADER = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}

HTTP_URL = (
    'http://www.x.com',
    'http://ip.cn',
    'http://ip.chinaz.com/',
    'http://www.wangsutong.com/wstCeba/http/http-test.action',
    'http://ce.cloud.360.cn/',
)

HTTPS_URL = (
    'https://www.baidu.com/',
    'http://cn.bing.com/',
    'https://www.sogou.com/',
    'https://www.so.com/'
)


def proxy1():
    """http"""
    url = 'http://www.kuaidaili.com/free/inha/'
    urls = [url + str(x) for x in range(1, 11)]
    for u in urls:
        tree = utils.htmltree(u)
        for x in tree.xpath('//tbody/tr'):
            yield 'http', ':'.join(x.xpath('td[1]/text() | td[2]/text()'))
            # 502 error occur if fetch too fast
            time.sleep(1)


def proxy2():
    """http"""
    url = 'http://www.xicidaili.com/wt/'
    urls = [url + str(x) for x in range(1, 6)]
    for u in urls:
        tree = utils.htmltree(u, headers=HEADER)
        for x in tree.xpath('//tr[@class="odd"]'):
            yield 'http', ":".join(x.xpath('td[2]/text() | td[3]/text()'))
            time.sleep(.1)


def proxy3():
    """https"""
    url = 'http://www.xicidaili.com/wn/'
    urls = [url + str(x) for x in range(1, 6)]
    for u in urls:
        tree = utils.htmltree(u, headers=HEADER)
        for x in tree.xpath('//tr[@class="odd"]'):
            yield 'https', ":".join(x.xpath('td[2]/text() | td[3]/text()'))
            time.sleep(.1)


def getproxy():
    from itertools import chain
    return chain(proxy1(), proxy2(), proxy3())


def validate(proxy, protocol='http', retry=True, delay=True):
    try:
        if protocol == 'http':
            url = random.choice(HTTP_URL)
            proxies = {'http:': 'http://' + proxy}
        elif protocol == 'https':
            url = random.choice(HTTPS_URL)
            proxies = {'https:': 'https://' + proxy}
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            print(proxy)
            return True
    except Exception as e:
        if retry:
            validate(proxy, protocol, retry=False)
        print(e)
        return False


if __name__ == '__main__':
    for p in getproxy():
        print(p)

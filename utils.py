# -*- coding: utf-8 -*-
"""
    parse.py
    ~~~~~~
    
    :license: MIT, see LICENSE for more details.
"""
from lxml import etree
import requests


def htmltree(url, headers=None, proxies=None):
    response = requests.get(url, headers=headers, proxies=proxies)
    tree = etree.HTML(response.text)
    return tree

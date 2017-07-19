# -*- coding: utf-8 -*-
"""
    tasks.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import

import sys
sys.path.append('../')

from celery_app.celery import app
import proxy
from db import queue


@app.task
def refresh():
    for (protocol, ip) in proxy.getproxy():
        if proxy.validate(ip, protocol):
            queue.push(ip, protocol)


@app.task
def validate():
    for protocol in ('http', 'https'):
        for i in range(queue.len(protocol)):
            ip = queue.get(protocol)
            if proxy.validate(ip, protocol):
                queue.push(ip, protocol)


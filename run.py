# -*- coding: utf-8 -*-
"""
    run.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""
from api.proxyapi import run
from celery_app.tasks import refresh
from db import queue


if __name__ == '__main__':
    # queue.init()
    # In celery beat you can't call the task at once,
    # so you should call it manually.
    refresh.delay()
    run()

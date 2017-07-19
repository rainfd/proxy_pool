# -*- coding: utf-8 -*-
"""
    celery.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import

from celery import Celery

app = Celery('celery_app', include=['celery_app.tasks'])
app.config_from_object('celery_app.celeryconfig')


if __name__ == '__main__':
    app.start()

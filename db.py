# -*- coding: utf-8 -*-
"""
    db.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""

import redis


class RedisQueue(object):

    def __init__(self, name):
        self.session = redis.Redis()
        self.name = name

    def init(self):
        self.session.delete(self.name)

    def get(self):
        return self.session.rpoplpush(self.name, self.name).decode()

    def pop(self):
        return self.session.rpop(self.name).decode()

    def push(self, value):
        return self.session.lpush(self.name, value)

    def __len__(self):
        return self.session.llen(self.name)

    def delete(self, value):
        self.session.lrem(self.name, 1, value)


class ProxyQueue(object):

    def __init__(self):
        self.http = RedisQueue('http')
        self.https = RedisQueue('https')

    def init(self):
        self.http.init()
        self.https.init()

    def get(self, protocol='http'):
        return getattr(self, protocol).get()

    def pop(self, protocol='http'):
        return getattr(self, protocol).pop()

    def push(self, value, protocol='http'):
        getattr(self, protocol).push(value)

    def len(self, protocol='http'):
        return len(getattr(self, protocol))

    def delete(self, value, protocol='http'):
        getattr(self, protocol).delete(value)


queue = ProxyQueue()

# -*- coding: utf-8 -*-
"""
    proxyapi.py
    ~~~~~~

    :license: MIT, see LICENSE for more details.
"""
import sys
sys.path.append('..')

import json
from flask import Flask, jsonify, redirect, url_for, request, Response
from db import queue
from celery_app.tasks import refresh



app = Flask(__name__)


api_list = {
    'get/http/1': 'get an usable proxy',
    'getall/http': 'get all proxy',
    'status': 'proxy number',
    'delete?proxy=127.0.0.1:8080?protocol=http': 'delete an unable proxy'
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/')
@app.route('/get/<int:number>/')
@app.route('/get/<string:protocol>/')
@app.route('/get/<string:protocol>/<int:number>/')
def get(protocol='http', number=1):
    length = queue.len(protocol)
    if number > length:
        number = length
    proxies = [queue.get(protocol=protocol) for i in range(number)]
    return Response(json.dumps(proxies), mimetype='application/json')


@app.route('/getall/')
@app.route('/getall/<string:protocol>/')
def getall(protocol='http'):
    return redirect(url_for('get', protocol=protocol, number=queue.len(protocol)))


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    protocol = request.args.get('protocol', 'http')
    if proxy.validate(proxy, protocol):
        queue.delete(proxy, protocol)
        return 'Done'


@app.route('/refresh/')
def fresh():
    refresh.delay()


@app.route('/status/')
def status():
    length = {
        'http': queue.len('http'),
        'https': queue.len('https')
    }
    return jsonify(length)


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run()

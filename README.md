# proxy_pool

a simple proxy pool

Fetch proxies and parse them, then store in redis queue.
Use celery to schedule refresh and validate task on a regular interval.

```
$ sudo apt-get install redis-server
$ pip install -r requirement
$ celery -B -A celery_app worker -l warning -f beat.log

$ python run.py

```
api_list on `0.0.0.0:5000`

get a http proxy: `/get/http/1`

import redis
from time import time


class UrlQueue(object):
    def __init__(self, **kwargs):
        host = kwargs.get('host', '127.0.0.1')
        port = kwargs.get('port', 6379)
        db = kwargs.get('db', 13)
        self.site = kwargs.get('site')
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=True, db=db)
        self.redis = redis.StrictRedis(connection_pool=pool)

    def add_url(self, post_id, time_delta=0):
        self.redis.zadd(self.site, {post_id: int(time()) + time_delta})

    def get_url(self):
        success, url, num_proxies = self.attempt_url_lock(site=self.site, min_gap=0)
        while not success:
            success, url, num_proxies = self.attempt_url_lock(site=self.site, min_gap=0)
            print('waiting url!')
        print('total {} url are usefully in past 24 hours'.format(num_proxies))
        return url

    def attempt_url_lock(self, min_gap=0, site='dp_star'):
        with self.redis.pipeline() as pipe:
            try:
                pipe.watch(site)
                available = pipe.zrangebyscore(site, time() - 3600 * 24, time())
                if available:
                    url = available[0]
                    pipe.multi()
                    pipe.zadd(site, {url: time() + 3600 * 0.5})
                    pipe.execute()
                    return True, url, len(available)
                return True, None, 0
            except redis.WatchError:
                return None, None, 0

    def process_success(self, post_id):
        self.redis.zadd(self.site, {post_id: time() - 3600 * 72})

    def process_failure(self, post_id):
        self.redis.zadd(self.site, {post_id: time() + 3600 * 0.5})

    def get_url_num(self):
        start = time() - 3600 * 24
        end = time() + 3600 * 24
        num = self.redis.zrangebyscore(self.site, start, end)
        return len(num)

    def delete_url(self):
        self.redis.delete(self.site)

import app

class RedisWrapper(object):
    db = None

    def __getattr__(self, name):
        return getattr(self.db, name)

class TestRedis(RedisWrapper):
    db = app.redis_test

class ProdRedis(RedisWrapper):
    db = app.redis_prod

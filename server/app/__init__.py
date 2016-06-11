import redis
from config import Config as config

redis_test = redis.StrictRedis(config.REDIS_CACHE_SERVER, db=0)
redis_prod = redis.StrictRedis(config.REDIS_CACHE_SERVER, db=1)

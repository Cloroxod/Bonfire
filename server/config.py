
class Config(object):
    LIVE = False

    REDIS_CACHE_SERVER = 'localhost'

    CONNECTIONS = {
        'main': {
            'host': 'localhost',
            'port': 12345
        },
    }

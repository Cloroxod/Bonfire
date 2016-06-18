from app.utilities.location import LocationManager
from app.utilities.redis import TestRedis
from build import report_pb2
import time

class MessageHandler(object):
    location_manager = LocationManager(TestRedis())
    redis = TestRedis()

    @classmethod
    def handle_update(cls, message):
        if message.type == report_pb2.POST:
            cls.handle_post(message)
        elif message.type == report_pb2.SEARCH:
            cls.handle_search(message)

    @classmethod
    def handle_post(cls, message):
        print 'Adding message: name=%s, latitude=%s, longitude=%s, content=%s' \
              % (message.name, message.latitude, message.longitude, message.content)
        cls.location_manager.add(message.latitude, message.longitude, message.content)
        cls.redis.set(time.time(), message.SerializeToString())

    @classmethod
    def handle_search(cls, message):
        results = cls.location_manager._search(message.latitude, message.longitude, 0, 3, 100000)
        print 'Result from search: ', results
        result_msg = report_pb2.SearchResult()
        for search_result in results:
            result_msg.messages.add().content = search_result[0]

        return result_msg


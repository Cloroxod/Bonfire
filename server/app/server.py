from SocketServer import TCPServer, BaseRequestHandler, ThreadingMixIn
import socket
import threading
import subprocess
import message_handler
from build import report_pb2


class TCPHandler(BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread
        resp = '{}: {}'.format(cur_thread, data)  # TODO, parse + respond.

        post_message = report_pb2.Message()
        post_message.name = 'Chicago'
        post_message.latitude = 41.8781
        post_message.longitude = -87.6298
        post_message.content = 'Be wary of monster'
        post_message.type = report_pb2.POST
        message_handler.MessageHandler.handle_update(post_message)

        post_message2 = report_pb2.Message()
        post_message2.name = 'Lakeview'
        post_message2.latitude = 41.9436
        post_message2.longitude = -87.6584
        post_message2.content = 'Be wary of monster!!!'
        post_message2.type = report_pb2.POST
        message_handler.MessageHandler.handle_update(post_message2)

        post_message3 = report_pb2.Message()
        post_message3.name = 'Westmont'
        post_message3.latitude = 41.7969
        post_message3.longitude = -87.9756
        post_message3.content = 'WESTMONT!!'
        post_message3.type = report_pb2.POST
        message_handler.MessageHandler.handle_update(post_message3)

        search_message = report_pb2.Message()
        search_message.latitude = 41.7969
        search_message.longitude = -87.6584
        search_message.type = report_pb2.SEARCH
        message_handler.MessageHandler.handle_update(search_message)

        self.request.sendall(resp)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Server(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True


def get_server(conn):
    return Server(conn, TCPHandler)

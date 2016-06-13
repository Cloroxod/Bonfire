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
        post_message.name = 'Test message'
        post_message.latitude = 123
        post_message.longitude = 321
        post_message.content = 'Be wary of monster'
        message_handler.MessageHandler.handle_post(post_message)

        print resp
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

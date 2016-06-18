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

        update_message = report_pb2.Message()
        update_message.ParseFromString(data)

        if update_message.type == report_pb2.POST:
            message_handler.MessageHandler.handle_post(update_message)
        elif update_message.type == report_pb2.SEARCH:
            search_message = message_handler.MessageHandler.handle_search(update_message)
            self.request.sendall(search_message.SerializeToString())


        # self.request.sendall(resp)


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

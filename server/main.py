from app.server import get_server
from config import Config as config
import threading
import sys, os, signal

def run():
    main_connection = config.CONNECTIONS['main']
    HOST, PORT = main_connection['host'], main_connection['port']

    server = get_server((HOST, PORT))
    ip, port = server.server_address

    try:
        'Starting Server. . .'
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.close()
        sys.exit(0)

def exit_handler(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    run()

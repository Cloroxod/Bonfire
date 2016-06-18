import socket
import time
from build import report_pb2

ip = 'localhost'
port = 12345


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

if __name__ == '__main__':

    post_message = report_pb2.Message()
    post_message.name = 'Chicago'
    post_message.latitude = 41.8781
    post_message.longitude = -87.6298
    post_message.content = 'Be wary of monster'
    post_message.type = report_pb2.POST
    post_message.timestamp = time.time()
    test_post = post_message.SerializeToString()
    client(ip, port, test_post)

    post_message2 = report_pb2.Message()
    post_message2.name = 'Lakeview'
    post_message2.latitude = 41.9436
    post_message2.longitude = -87.6584
    post_message2.content = 'Be wary of monster!!!'
    post_message2.type = report_pb2.POST
    post_message2.timestamp = time.time()
    test_post = post_message2.SerializeToString()
    client(ip, port, test_post)

    post_message3 = report_pb2.Message()
    post_message3.name = 'Westmont'
    post_message3.latitude = 41.7969
    post_message3.longitude = -87.9756
    post_message3.content = 'WESTMONT!!'
    post_message3.type = report_pb2.POST
    post_message3.timestamp = time.time()
    test_post = post_message3.SerializeToString()
    client(ip, port, test_post)

    update_message = report_pb2.Message()
    update_message.latitude = 41.7969
    update_message.longitude = -87.6584
    update_message.type = report_pb2.SEARCH
    test_post = update_message.SerializeToString()
    client(ip, port, test_post)

    # client(ip, port, str(0))

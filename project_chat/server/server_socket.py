from socket import *


class ServerSocket:
    def __init__(self, sock):
        self.sock = sock

    def send(self, msg):
        self.sock.send(msg)


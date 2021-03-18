from socket import *


class ClientSocket:
    def __init__(self, sock):
        self.sock = sock

    def send(self, msg):
        self.sock.send(msg)

    # def recv(self):
    #     self.sock.recv(10000)

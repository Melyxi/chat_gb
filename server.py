# server

# Программа сервера времени
import datetime
from socket import *
import time
import click
from contextlib import closing
import json
import os

from project_chat.server.db.db import ObjRelMap
from project_chat.server.serializer import Serializer
from project_chat.server.server_socket import ServerSocket
#from project_chat.server.server import Server
import project_chat.server.server_log_config
import selectors
import errno
import logging
import socket
from project_chat.server.server import FeedData
logger = logging.getLogger('server')
import select

LIMIT_BYTE = 640



class Port:
    """
    Класс-дескриптор для порта. Проверяет, входит ли адрес в допустимый диапазон (с 1024 до 65535).
    """
    def __set__(self, instance, value):
        #print("__set__")
        if not (1023 < value < 65535):
            logger.critical(f'Допустимы адреса с 1024 до 65535. Передан {value}')
            raise TypeError('Некорректрый номер порта')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        #print('name')
        self.name = name


class Server:
    port = Port()

    def __init__(self, addr, port, db_url):

        self.addr = addr
        self.port = port

        self.db_url = db_url
        self.clients = []
        self.auth_clients = []
        self.sock = None


    def init_sock(self):
        sock = socket.socket(AF_INET, SOCK_STREAM)
        sock.bind((self.addr, self.port))  # Присваивает порт 8800
        sock.listen(100)  # одновременно обслуживает не более
        sock.settimeout(0.2)

        self.sock = sock

    def accept(self):
        return self.sock.accept()

    def disconnect_client(self, sock, all_clients):
        print(f"Клиент‚ {sock.fileno()} {sock.getpeername()} отключился")
        sock.close()
        all_clients.remove(sock)

    def read_requests(self, r_clients, all_clients):

        responses = {}
        for sock in r_clients:
            try:
                data = sock.recv(640)

                feed_data = FeedData(data, self.db_url)
                byte_str = feed_data.analysis_data()
                responses[sock] = byte_str

                if feed_data.auth_code:
                    self.auth_clients.append(sock)

            except:

                self.disconnect_client(sock, all_clients)

        return responses

    def write_responses(self, requests, w_clients, all_clients):

        for sock in w_clients:
            if sock in self.auth_clients:
                for recv_sock, data in requests.items():
                    recv = Serializer().serializer_client(data)


                    if sock is recv_sock:
                        if recv['action'] != 'message':
                            sock.send(data)
                        continue

                    try:
                        if recv['action'] == 'message':
                            sock.send(data)
                        print(json.loads(data.decode("utf-8")))
                    except:
                        self.disconnect_client(sock, all_clients)
            else:
                if sock in requests:
                    data = requests[sock]
                    # print('noaut')
                    sock.send(data)



@click.command()
@click.option('--a', default='', help='ip')
@click.option('--p', default=7777, help='port')
def main(a, p):
    path = os.path.join(os.getcwd(), 'project_chat/server/db/company.db3') # бд
    print(a, p)
    server = Server(a, p, path)
    server.init_sock()

    while True:
        try:

            client, addr = server.accept()  # Принять запрос на соединение
            logger.info("connect server")
        except OSError:
            pass
        else:
            logger.debug(f"Клиент подключился")
            print(f"Клиент подключился‚ {addr}")

            print(addr)

            path = os.path.join(os.getcwd(), 'project_chat/server/db/company.db3')
            time_at = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            list_data = {'username_id': 1, 'ip_addr': str(addr), 'time_at': time_at}
            cliendb = ObjRelMap(path)
            cliendb.add('HistoryClient', list_data)

            server.clients.append(client)
        finally:

            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(server.clients, server.clients, [], wait)
            except:
                pass

            requests = server.read_requests(r, server.clients)
            server.write_responses(requests, w, server.clients)


if __name__ == '__main__':
    main()

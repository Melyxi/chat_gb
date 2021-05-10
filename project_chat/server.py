# server
import datetime
import logging
import os
import select
import socket
import time
from socket import *

import click
from server.db.db import ObjRelMap
from server.serializer import Serializer
from server.server import FeedData

logger = logging.getLogger('server')


LIMIT_BYTE = 640



class Port:
    """
    Класс-дескриптор для порта. Проверяет, входит ли адрес в допустимый диапазон (с 1024 до 65535).
    """
    def __set__(self, instance, value):
        if not (1023 < value < 65535):
            logger.critical(f'Допустимы адреса с 1024 до 65535. Передан {value}')
            raise TypeError('Некорректрый номер порта')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
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
                    except:
                        self.disconnect_client(sock, all_clients)
            else:
                if sock in requests:
                    data = requests[sock]
                    sock.send(data)



@click.command()
@click.option('--a', default='', help='ip')
@click.option('--p', default=7777, help='port')
def main(a, p):
    g = os.path.dirname(os.path.abspath(__file__))
    path = g + '\\server\\db\\company.db3'
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

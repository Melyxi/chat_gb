# server

# Программа сервера времени
from socket import *
import time
import click
from contextlib import closing
import json
import os
from project_chat.server.serializer import Serializer
from project_chat.server.server_socket import ServerSocket
from project_chat.server.server import Server
import project_chat.server.server_log_config
import selectors
import errno
import logging
import socket
from project_chat.server.server import FeedData
logger = logging.getLogger('server')
import select

LIMIT_BYTE = 640


class Process:

    def __init__(self):
        self.clients = []
        self.auth_clients = []

    def disconnect_client(self, sock, all_clients):
        print(f"Клиент‚ {sock.fileno()} {sock.getpeername()} отключился")
        sock.close()
        all_clients.remove(sock)

    def read_requests(self, r_clients, all_clients):

        responses = {}
        for sock in r_clients:
            try:
                data = sock.recv(640)

                # новый код
                feed_data = FeedData(data)
                byte_str = feed_data.analysis_data()
                responses[sock] = byte_str

                if feed_data.auth_user():
                    self.auth_clients.append(sock)
                # новый код
            except:
                self.disconnect_client(sock, all_clients)

        return responses



    def write_responses(self, requests, w_clients, all_clients):

        for sock in w_clients:
            if sock in self.auth_clients:
                for recv_sock, data in requests.items():
                    if sock is recv_sock:
                        recv = Serializer().serializer_client(data)
                        if 'action' in recv and recv['action'] == "authenticate":
                            sock.send(data)
                        continue

                    try:
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

    with socket.socket(AF_INET, SOCK_STREAM) as s:  # Создает сокет TCP
        s.bind((a, p))  # Присваивает порт 8800
        s.listen(5)  # одновременно обслуживает не более
        s.settimeout(0.2)  # Переходит в режим ожидания запросов;
        # 5 запросов.
        process = Process()
        while True:
            try:
                client, addr = s.accept()  # Принять запрос на соединение
                logger.info("connect server")
            except OSError:
                pass
            else:
                logger.debug(f"Клиент подключился")
                print(f"Клиент подключился‚ {addr}")
                process.clients.append(client)
            finally:

                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(process.clients, process.clients, [], wait)
                except:
                    pass

                requests = process.read_requests(r, process.clients)
                process.write_responses(requests, w, process.clients)


if __name__ == '__main__':
    main()

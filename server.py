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

import logging

logger = logging.getLogger('server')

LIMIT_BYTE = 640

@click.command()
@click.option('--a', default='', help='ip')
@click.option('--p', default=7777, help='port')
def main(a, p):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создает сокет TCP
        s.bind((a, p))  # Присваивает порт 8800
        s.listen(5)  # Переходит в режим ожидания запросов;
                        # одновременно обслуживает не более
                        # 5 запросов.
        while True:
            client, addr = s.accept()  # Принять запрос на соединение
            logger.info("connect server")
            with closing(client) as cl:
                client_server = ServerSocket(cl)
                server = Server(client_server, Serializer()) # объект сервер
                while True:
                    data = cl.recv(LIMIT_BYTE)

                    code = Serializer().serialize_server_authenticate_code(data) # получаем код аунтификации
                    recv_message = Serializer().serializer_client(data) # получаем сообщение от клиента
                    logger.debug(f"Аунтификация")
                    print('Сообщение: ', recv_message, ', было отправлено клиентом: ', addr, 'количество байтов', len(data))


                    if code == '200':
                        server.authenticate(data)  # оправляем собщение аунтификации клиенту
                        logger.debug(f"Пользователь {recv_message['user']['account_name']} авторизовался")

                        while True:
                            data = cl.recv(LIMIT_BYTE)
                            recv_message = Serializer().serializer_client(data) # получаем сообщение от клиента
                            logger.debug(f"Сообщение от клиента получено")
                            print('Сообщение: ', recv_message, ', было отправлено клиентом: ', addr, 'количество байтов', len(data))

                            if recv_message['message'] == 'quit':
                                server.message(data) # оправляем собщение клиенту
                                logger.debug(f"Сообщаем о выходе пользователя")
                                break

                            else:
                                server.message(data)  # оправляем собщение клиенту
                                logger.debug(f"Ответ клиенту от сервера")


                    elif code == '402':

                        server.authenticate(data)  # оправляем собщение аунтификации клиенту
                        logger.debug(f"Неверный пароль или имя пользователя")

                    elif code == '403':

                        server.authenticate(data)  # оправляем собщение аунтификации клиенту
                        logger.debug(f"Неверно введены данные")




if __name__ == '__main__':
    main()

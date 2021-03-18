import click
from socket import *
import datetime, time
import json
from project_chat.client.client_socket import ClientSocket
from project_chat.client.serializer import Serializer
from project_chat.client.client import Client
import project_chat.client.client_log_config
import logging

logger = logging.getLogger('client')

LIMIT_BYTE = 640
@click.command()
@click.option('--add', default='localhost', help='ip')
@click.option('--port', default=7777, help='port')
@click.option('--recv/--send', default=True, help='mode')
def main(add, port, recv):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        s.connect((add, port))
        logger.info("connect socket")
        client_sock = ClientSocket(s)
        while True:
            account_name = input("Введите имя: ")
            client = Client(client_sock, account_name, Serializer())  # передаем сокет, имя, серилизатор
            password = input("Введите пароль: ")
            client.authenticate(password)  # проходим аунтификацию вводим пароль

            data = s.recv(LIMIT_BYTE)
            #print('data')
            dict_server = Serializer().serializer_code(data)

            code = Serializer().serializer_code_authenticate(data)
            print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

            while code == 200:
                logger.info(f"connect client {account_name}")

                if recv:
                    data = s.recv(LIMIT_BYTE)
                    dict_server = Serializer().serializer_code(data)

                    print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')
                else:

                    msg = input("Введите сообщение: ")
                    to_user = "#room"

                    client.message(msg=msg, to_user=to_user)  # вводим сообщение
                    if msg == 'quit':
                        logger.info(f"пользователь: {account_name}, вышел")
                        break


if __name__ == '__main__':
    main()


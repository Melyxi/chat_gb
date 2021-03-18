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
def main(add, port):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        s.connect((add, port))
        logger.info("connect socket")
        client_sock = ClientSocket(s)
        while True:
            account_name = input("Введите имя: ")
            client = Client(client_sock, account_name, Serializer())  # передаем сокет, имя, серилизатор
            password = input("Введите пароль: ")
            client.authenticate(password)  # проходим аунтификацию вводим пароль

            try:
                data = s.recv(LIMIT_BYTE)
                dict_server = Serializer().serializer_code(data)
                logger.debug(f'Сообщение от сервера {dict_server}')
            except BaseException as e:
                logger.exception(f"Error! {e}")

            code = Serializer().serializer_code_authenticate(data)
            print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

            while code == 200:
                logger.info(f"connect client {account_name}")
                msg = input("Введите сообщение: ")
                to_user = "#room"
                try:
                    client.message(msg=msg, to_user=to_user)  # вводим сообщение
                    logger.debug(f"Сообщение отправлено, пользователем: {account_name}, кому: {to_user}")
                except BaseException as e:
                    logger.exception(f"Сообщение не отправлено")
                data = s.recv(LIMIT_BYTE)

                try:
                    dict_server = Serializer().serializer_code(data)
                    logger.debug(f'Сообщение от сервера {dict_server}')
                except BaseException as e:
                    logger.exception(f"Error! {e}")

                print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

                if msg == 'quit':
                    logger.info(f"пользователь: {account_name}, вышел")
                    break


if __name__ == '__main__':
    main()


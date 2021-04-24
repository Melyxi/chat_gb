import click
from socket import *
import datetime, time
import json
from project_chat.client.client_socket import ClientSocket
from project_chat.client.serializer import Serializer
from project_chat.client.client import Client
import project_chat.client.client_log_config
import logging
import threading

logger = logging.getLogger('client')


import os
import sys
import threading
from pathlib import Path

import PyQt5
from PyQt5.QtWidgets import QLineEdit
from icecream import ic
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets

def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, iu):
        super().__init__()

        self._iu = iu
        ui_file_path = Path(__file__).parent.absolute() / "client.ui"
        uic.loadUi(ui_file_path, self)
        self.log = None
        self.pas = None
        self.dict_data = None
        self.flag_btn = False
        btn = self.pushLogin.clicked.connect(lambda: self.push_data)
        self.Password.setEchoMode(QLineEdit.Password)
        self.Login.textChanged.connect(self.on_text_login)
        self.Password.textChanged.connect(self.on_text_password)


    def on_text_login(self):
        self.log = self.Login.text()
        #print(self.log)
        self.Login.text()

    def on_text_password(self):
        self.pas = self.Password.text()
        #print(self.pas)
        self.Password.text()

    def push_data(self):
        self.flag_btn = True
        self.dict_data = {'login': self.log, 'password': self.pas}

        return self.dict_data

    def event(self, e):

        if e.type() == QtCore.QEvent.btn:
            print("Нажата клавиша на клавиатуре")
            print("Код:", e.key(), ", текст:", self.push_data())
        elif e.type() == QtCore.QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            print("Клик мышью. Координаты:", e.x(), e.y())

        print(super().event(e))
        # Событие отправляется дальше
        return super().event(e)

class NewChatMsgEvent(QtCore.QEvent):
    def __init__(self, from_user, msg, tm):
        super().__init__(QtCore.QEvent.User)
        self._from_user = from_user
        self._msg = msg
        self._tm = tm


class DisconnectedFromServerEvent(QtCore.QEvent):
    def __init__(self):
        super().__init__(QtCore.QEvent.User)


class EventHandler(QtCore.QObject):

    def event(self, e) -> bool:
        if e.type() == QtCore.QEvent.User:
            if isinstance(e, DisconnectedFromServerEvent):

                print(f"Disconnect event")
            elif isinstance(e, NewChatMsgEvent):
                pass
        return super().event(e)


class UiNotifier:
    def __init__(self, app, handler) -> None:
        self._app = app
        self._handler = handler

    def notify_disconnect(self):
        self._app.postEvent(self._handler, DisconnectedFromServerEvent())
        print('print notifielr')

    def notify_new_chat_msg(self, from_user, msg, tm):
        self._app.postEvent(self._handler, NewChatMsgEvent(from_user, msg, tm))



def mainloop(mw, app, handler):
    ui = UiNotifier(app, handler)

    print(mw.log)
    ui.notify_disconnect()






    #print(data, 'data')

def recv_msg(client):

    s = client._client_socket.sock

    data = s.recv(LIMIT_BYTE)
    dict_server = Serializer().serializer_code(data)
    print(f"Сообщение от сервера: {dict_server} длиной {len(data)} байт")
    #print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')





def send_message(client):
    action = input("Введите действие: ")

    if action == 'add':
        cl = input('Введите имя клиента ')
        client.add_contact(cl)

    elif action == 'del':
        cl = input('Введите имя клиента ')
        client.del_contact(cl)

    elif action == 'get':
        client.get_contacts()
    else:
        account_name = client.account_name
        msg = input("Введите сообщение: ")
        to_user = "#room"

        client.message(msg=msg, to_user=to_user)  # вводим сообщение
        if msg == 'quit':

            logger.info(f"пользователь: {account_name}, вышел")



LIMIT_BYTE = 640
@click.command()
@click.option('--add', default='localhost', help='ip')
@click.option('--port', default=7777, help='port')
#@click.option('--recv/--send', default=True, help='mode')
def main(add, port):
    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        #print('+-+-+-+')
        s.connect((add, port))
        logger.info("connect socket")
        client_sock = ClientSocket(s)

        while True:

            account_name = input("Введите имя: ")
            client = Client(client_sock, account_name, Serializer())  # передаем сокет, имя, серилизатор

            # проходим аунтификацию
            password = input("Введите пароль: ")
            client.authenticate(password)  # проходим аунтификацию вводим пароль


            data = s.recv(LIMIT_BYTE)
            #print('data')
            dict_server = Serializer().serializer_code(data)

            code = Serializer().serializer_code_authenticate(data)
            print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

            while code == 200:



                logger.info(f"connect client {account_name}")
                # Запускает клиентский процесс приёма сообщений
                #print('** Запуск потока \'thread-1\' для приёма сообщений **')

                receiver = threading.Thread(target=recv_msg, args=(client,))
                receiver.daemon = True
                receiver.start()

                # Запускает отправку сообщений и взаимодействие с клиентом
                #print('** Запуск потока \'thread-2\' для отправки сообщений **')
                user_interface = threading.Thread(target=send_message, args=(client, ))
                user_interface.daemon = True
                user_interface.start()
                
                while True:
                    time.sleep(1)
                    if receiver.is_alive() and user_interface.is_alive():
                        continue
                    break

if __name__ == '__main__':
    main()
    setup_plugin_path()


    app = QtWidgets.QApplication(sys.argv)
    handler = EventHandler()
    iu = UiNotifier(app, handler)

    mw = MainWindow(iu)
    mw.show()

    thr = threading.Thread(target=mainloop, args=(mw, app, handler))
    thr.start()

    app.exec_()
    thr.join()
    # thr.join()

import click
from socket import *
import datetime, time
import json

from PyQt5.QtCore import Qt
from psutil._common import addr

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
from PyQt5.QtWidgets import QLineEdit, QTableWidgetItem
from icecream import ic
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui, QtWidgets

def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)



class DialogWindow(QtWidgets.QMainWindow):

    def __init__(self, to_client, client=None):
        super().__init__()

        self._to_client = to_client
        ui_file_path = Path(__file__).parent.absolute() / "project_chat\\client\\front\\dialog1.ui"
        uic.loadUi(ui_file_path, self)
        self.msg = None

        self.setWindowTitle(self._to_client)

        self._client = client

        self.pushMsg.clicked.connect(self.push_msg)

        self.textmsg.textChanged.connect(self.on_text_msg)

        self.chat.setReadOnly(True)

        self.client_sock = None
        self.ch = None
        self.s = None


        receiver = threading.Thread(target=self.recv_msg_dlg, args=())
        receiver.daemon = True
        receiver.start()

        # Запускает отправку сообщений и взаимодействие с клиентом
        # print('** Запуск потока \'thread-2\' для отправки сообщений **')
        # user_interface = threading.Thread(target=self.send_message, args=())
        #
        # user_interface.start()



    def on_text_msg(self):
        self.msg = self.textmsg.toPlainText()
        print(self.msg)


    def push_msg(self):
        account_name = self._client.account_name
        msg = self.msg

        self.chat.setTextColor(Qt.blue)
        self.chat.append(f'{account_name}: {msg}')

        print(type(self.msg), 'send')
        to_user = self._to_client
        self._client.message(msg=msg, to_user=to_user)  # вводим сообщение
        if msg == 'quit':
            logger.info(f"пользователь: {account_name}, вышел")
        self.textmsg.clear()


    def recv_msg_dlg(self):
        while True:
            print('recv')
            s = self._client._client_socket.sock

            data = s.recv(LIMIT_BYTE)
            dict_server = Serializer().serializer_code(data)

            print(dict_server)

            if 'сообщение' in dict_server:
                print('222')

                self.chat.setTextColor(Qt.red)
                self.chat.append(f": {dict_server['сообщение']}")


            #f'{account_name}: {msg}'
            print(f"Сообщение от сервера: {dict_server} длиной {len(data)} байт message")



class MainChat(QtWidgets.QMainWindow):

    dlg = {}
    def __init__(self, client):
        super().__init__()

        self._client = client
        ui_file_path = Path(__file__).parent.absolute() / "project_chat\\client\\front\\mainchat.ui"
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle(self._client.account_name)



        # receiver = threading.Thread(target=self.revc, args=())
        # receiver.daemon = True
        # receiver.start()
        self._client.get_contacts()
        self.get()

        # user_interface = threading.Thread(target=self.send_message, args=())
        # user_interface.daemon = True
        # user_interface.start()

        self.addEdit.textChanged.connect(self.text_add_client)
        self.deleteEdit.textChanged.connect(self.text_del_client)

        self.addButton.clicked.connect(self.push_add_client)
        self.deleteButton.clicked.connect(self.push_del_client)

        self.addEdit_client = None
        self.delEdit_client = None
        self.tableWidget.setColumnCount(1)

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setHorizontalHeaderLabels(['Друзья'])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.cellDoubleClicked.connect(self.take_item)

    def push_add_client(self):
        self._client.add_contact(self.addEdit_client)
        self.addEdit.clear()
        self._client.get_contacts()
        self.get()

    def push_del_client(self):
        self._client.del_contact(self.delEdit_client)
        self.deleteEdit.clear()
        self._client.get_contacts()
        self.get()


    def text_add_client(self):
        self.addEdit_client = self.addEdit.text()
        print(self.addEdit_client)
        self.addEdit.text()


    def text_del_client(self):
        self.delEdit_client = self.deleteEdit.text()
        print(self.delEdit_client)
        self.deleteEdit.text()

    # def send_message(self):
    #     while True:
    #         print('send')
    #         self._client.get_contacts()
    #         time.sleep(10)

    def get(self):
        self._client.get_contacts()
        self.s = self._client._client_socket.sock
        data = self.s.recv(LIMIT_BYTE)

        dict_server = Serializer().serializer_code(data)
        print(f"Сообщение от сервера: {dict_server} длиной {len(data)} байт")

        if 'alert' in dict_server and 'action' in dict_server and dict_server['action'] == 'get_clients':
            self.show_client(dict_server['alert'])

    def revc(self):
        while True:
            self._client.get_contacts()
            self.s = self._client._client_socket.sock
            data = self.s.recv(LIMIT_BYTE)

            dict_server = Serializer().serializer_code(data)
            print(f"Сообщение от сервера: {dict_server} длиной {len(data)} байт")

            if 'alert' in dict_server and 'action' in dict_server and dict_server['action'] == 'get_clients':
                self.show_client(dict_server['alert'])

    # def recv_msg(self):
    #     while True:
    #         s = self._client._client_socket.sock
    #
    #         data = s.recv(LIMIT_BYTE)
    #         dict_server = Serializer().serializer_code(data)
    #         print(f"Сообщение от сервера: {dict_server} длиной {len(data)} байт")
    #
    #         if 'alert' in dict_server and 'action' in dict_server and dict_server['action'] == 'get_clients':
    #             self.show_client(dict_server['alert'])
    #         # print('Сообщение от сервера: ', dict_server, ', длиной ', len(data), ' байт')

    def show_client(self, client_list):
        self.tableWidget.setRowCount(len(client_list))
        for i, rev in enumerate(client_list):
            self.tableWidget.setItem(0, i, QTableWidgetItem(rev))


    def take_item(self, row, column):
        item = self.tableWidget.item(row, column)

        from_user = item.text()
        dialog = DialogWindow(from_user, self._client)

        self.dlg[from_user] = dialog
        self.print_dlg(from_user)


    def print_dlg(self, from_user):
        self.dlg[from_user].show()


    def event(self, e):

        if e.type() == QtCore.QEvent.Close:
            print(self.dlg)

        elif e.type() == QtCore.QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            print("Клик мышью. Координаты:", e.x(), e.y())

        # Событие отправляется дальше
        return super().event(e)


class MainWindow(QtWidgets.QMainWindow):



    def __init__(self):
        super().__init__()


        ui_file_path = Path(__file__).parent.absolute() / "project_chat\\client\\front\\client.ui"
        uic.loadUi(ui_file_path, self)
        self.log = None
        self.pas = None
        self.dict_data = None
        self.flag_btn = False
        self.pushLogin.clicked.connect(self.push_data)

        self.Password.setEchoMode(QLineEdit.Password)

        self.Login.textChanged.connect(self.on_text_login)
        self.Password.textChanged.connect(self.on_text_password)

        self.client_sock = None
        self._client = None





        self.s = None

        self.connection()


    def on_text_login(self):
        self.log = self.Login.text()
        print(self.log)
        self.Login.text()

    def on_text_password(self):
        self.pas = self.Password.text()
        print(self.pas)
        self.Password.text()





    def push_data(self):

        self.flag_btn = True
        self.dict_data = {'login': self.log, 'password': self.pas}

        self._client = Client(self.client_sock, self.log, Serializer())
        self._client.authenticate(self.pas)

        data = self.s.recv(LIMIT_BYTE)
        dict_server = Serializer().serializer_code(data)
        print(self.log)
        code = Serializer().serializer_code_authenticate(data)
        print(code, 'code')
        if code == 200:
            #self.dialog = DialogWindow(client)
            self.MainChat = MainChat(self._client)
            print('Вошли')
            self.statusBar().showMessage('Вошли')
            self.statusBar().setGeometry(200, 80, 400, 20)
            self.MainChat.show()
            #self.dialog.show()


        elif code == 402:
            print("Неверный пароль или логин")
            self.statusBar().showMessage('Неверный пароль или логин')
            self.statusBar().setGeometry(150, 80, 400, 20)


    def event(self, e):

        if e.type() == QtCore.QEvent.Close:
            print("Нажата клавиша на клавиатуре")

        elif e.type() == QtCore.QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QtCore.QEvent.MouseButtonPress:
            print("Клик мышью. Координаты:", e.x(), e.y())


        # Событие отправляется дальше
        return super().event(e)

    def connection(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(('127.0.0.1', 7777))
        #s.connect((add, port))
        logger.info("connect socket")
        self.client_sock = ClientSocket(self.s)


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
def main(add, port, account_name, password):

    with socket(AF_INET, SOCK_STREAM) as s:  # Создать сокет TCP
        #print('+-+-+-+')
        s.connect((add, port))
        logger.info("connect socket")
        client_sock = ClientSocket(s)

        while True:


            #account_name = input("Введите имя: ")
            client = Client(client_sock, account_name, Serializer())  # передаем сокет, имя, серилизатор

            # проходим аунтификацию
            #password = input("Введите пароль: ")
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

def mainloop():



    mw = MainWindow()

    print(mw.log)





if __name__ == '__main__':

    setup_plugin_path()
    app = QtWidgets.QApplication(sys.argv)
    handler = EventHandler()
    iu = UiNotifier(app, handler)

    mw = MainWindow()
    mw.show()
    #thr = threading.Thread(target=mainloop, args=())
    #thr.start()

    app.exec_()
    #thr.join()
    # thr.join()

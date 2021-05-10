import sys
import threading
import time
from pathlib import Path
from socket import *

from PyQt5.QtCore import Qt
from icecream import ic

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QLineEdit
import os
from pathlib import Path

import PyQt5


from project_chat.client.client import Client
from project_chat.client.client_socket import ClientSocket
from project_chat.client.serializer import Serializer

LIMIT_BYTE = 640


class DialogWindow(QtWidgets.QMainWindow):

    def __init__(self, to_client, client=None):
        super().__init__()

        self._to_client = to_client
        ui_file_path = Path(__file__).parent.absolute() / "dialog1.ui"
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

    def on_text_msg(self):
        self.msg = self.textmsg.toPlainText()


    def push_msg(self):
        account_name = self._client.account_name
        msg = self.msg

        self.chat.setTextColor(Qt.blue)
        self.chat.append(f'{account_name}: {msg}')

        to_user = self._to_client
        self._client.message(msg=msg, to_user=to_user)  # вводим сообщение
        self.textmsg.clear()

    def recv_msg_dlg(self):
        while True:

            dict_server = Serializer().serializer_code(FeeData.dict_ser)

            client_name = self._client.account_name

            if 'сообщение' in dict_server and FeeData.dict_ser != b'[]':
                if self._to_client == dict_server['from'] and client_name == dict_server['to']:
                    self.chat.setTextColor(Qt.red)
                    self.chat.append(f"{self._to_client}: {dict_server['сообщение']}")
                    FeeData.dict_ser = b'[]'
                    time.sleep(0.5)


class MainChat(QtWidgets.QMainWindow):
    """
    :Class: main chat window
    :param client: type: Class: authorized client
    :param dlg: type: dict: dict dialog client
    """

    dlg = {}

    def __init__(self, client):
        super().__init__()

        self._client = client
        ui_file_path = Path(__file__).parent.absolute() / "mainchat.ui"
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle(self._client.account_name)

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

        self.get()

    def push_add_client(self):
        self._client.add_contact(self.addEdit_client)
        self.addEdit.clear()
        self.get()

    def push_del_client(self):
        self._client.del_contact(self.delEdit_client)
        self.deleteEdit.clear()
        self.get()

    def text_add_client(self):
        self.addEdit_client = self.addEdit.text()
        self.addEdit.text()

    def text_del_client(self):
        self.delEdit_client = self.deleteEdit.text()
        self.deleteEdit.text()

    def get(self):
        self._client.get_contacts()
        time.sleep(0.5)
        dict_server = Serializer().serializer_code(FeeData.dict_ser)

        if 'alert' in dict_server and 'action' in dict_server and dict_server['action'] == 'get_clients':
            self.show_client(dict_server['alert'])

    def show_client(self, client_list):
        self.tableWidget.setRowCount(len(client_list))
        for i, rev in enumerate(client_list):
            self.tableWidget.setItem(0, i, QTableWidgetItem(rev))

    def take_item(self, row, column):
        item = self.tableWidget.item(row, column)

        from_user = item.text()
        dialog = DialogWindow(from_user, self._client)

        if from_user in self.dlg:
            self.dlg[from_user].close()

        self.dlg[from_user] = dialog
        self.print_dlg(from_user)


    def print_dlg(self, from_user):
        self.dlg[from_user].show()


class MainWindow(QtWidgets.QMainWindow):
    """
    Class: login form chat
    :param sock: client socket
    """

    def __init__(self, sock):
        super().__init__()

        ui_file_path = Path(__file__).parent.absolute() / "client.ui"
        uic.loadUi(ui_file_path, self)
        self.log = None
        self.pas = None
        self.dict_data = None
        self.pushLogin.clicked.connect(self.push_data)

        self.Password.setEchoMode(QLineEdit.Password)

        self.Login.textChanged.connect(self.on_text_login)
        self.Password.textChanged.connect(self.on_text_password)

        self.s = sock
        self.client_sock = ClientSocket(self.s)
        self.io = IoLoop(self.s)

    def on_text_login(self):
        self.log = self.Login.text()
        self.Login.text()

    def on_text_password(self):
        self.pas = self.Password.text()
        self.Password.text()

    def push_data(self):

        self.flag_btn = True
        self.dict_data = {'login': self.log, 'password': self.pas}

        self._client = Client(self.client_sock, self.log, Serializer())
        self._client.authenticate(self.pas)

        time.sleep(0.5)
        code = Serializer().serializer_code_authenticate(FeeData.dict_ser)

        if code == 200:
            # self.dialog = DialogWindow(client)
            self.MainChat = MainChat(self._client)

            self.statusBar().showMessage('Вошли')
            self.statusBar().setGeometry(200, 80, 400, 20)
            self.MainChat.show()
            # self.dialog.show()


        elif code == 402:
            self.statusBar().showMessage('Неверный пароль или логин')
            self.statusBar().setGeometry(150, 80, 400, 20)


class FeeData:
    dict_ser = []

    def __init__(self, data):
        self._data = data
        self._dict_data = Serializer().serializer_code(data)

    @property
    def auth_code(self):
        return Serializer().serializer_code_authenticate(self.dict_ser)


class IoLoop:
    dict_server = []

    def __init__(self, s):
        self.s = s
        thr = threading.Thread(target=self.recv_msg, args=(s,))
        thr.start()

    def recv_msg(self, s):
        while True:
            data = s.recv(LIMIT_BYTE)
            FeeData.dict_ser = data
            self.dict_server = Serializer().serializer_code(data)




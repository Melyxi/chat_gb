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
from project_chat.client.front.front_client import MainWindow


def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)


if __name__ == '__main__':
    setup_plugin_path()
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    app.exec_()

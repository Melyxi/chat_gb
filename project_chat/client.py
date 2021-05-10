import os
import sys
from pathlib import Path
from socket import *

import click
import PyQt5
from client.front.front_client import MainWindow
from PyQt5 import QtWidgets


def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)


@click.command()
@click.option('--add', default='localhost', help='ip')
@click.option('--port', default=7777, help='port')
def main(add, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((add, port))

    setup_plugin_path()
    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow(s)
    mw.show()

    app.exec_()



if __name__ == '__main__':
    main()

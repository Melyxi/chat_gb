import sys
from pathlib import Path

from icecream import ic

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
import os
from pathlib import Path

import PyQt5


def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)




class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('server_gui.ui', self)


class Mytabl(MyWindow, QTableWidget):
    def __init__(self):
        MyWindow.__init__(self)
        #QTableWidget.__init__(self)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #window = MyWindow()
    w = Mytabl()
    w.show()
    #window.show()
    sys.exit(app.exec_())

    #window.btnQuit.clicked.connect(app.quit)
    #window.textEdit.textChanged.connect(lambda: ic(window.textEdit.toPlainText()))





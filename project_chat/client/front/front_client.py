import os
import sys
from pathlib import Path

import PyQt5
from icecream import ic
from PyQt5 import QtWidgets, uic

def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        ui_file_path = Path(__file__).parent.absolute() / "client.ui"
        uic.loadUi(ui_file_path, self)
        self.log = None
        self.pas = None
        self.pushLogin.clicked.connect(self.push_data)

        self.Login.textChanged.connect(self.on_text_login)
        self.Password.textChanged.connect(self.on_text_password)


    def on_text_login(self):
        self.log = self.Login.text()
        print(self.log)
        return self.Login.text()

    def on_text_password(self):
        self.pas = self.Password.text()
        print(self.pas)
        return self.Password.text()

    def push_data(self):
        self.dict_data = {'login': self.log, 'password': self.pas}

        return self.dict_data



if __name__ == "__main__":
    setup_plugin_path()

    app = QtWidgets.QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    data = app.exec_()
    print(mw.push_data(), 'push')
    #print(data, 'data')
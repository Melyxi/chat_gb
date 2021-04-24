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


if __name__ == "__main__":
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


    #print(data, 'data')
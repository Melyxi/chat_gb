import hmac

from .decor_log_server import log_msg, log_auth
import selectors
from .serializer import Serializer
import json
from .db.db import ObjRelMap, HistoryClient, ListClients, UserModel

"""
class Server:
    def __init__(self, client_socket, serializer):
        self._client_socket = client_socket
        self._serializer = serializer

    @log_auth
    def authenticate(self, byte_string):

        msg = self._serializer.serializer_answer_auth(byte_string)
        self._client_socket.send(msg)

    @log_msg
    def message(self, data):
        msg = self._serializer.serializer_server_message(data)
        self._client_socket.send(msg)

    def read(self):
        pass
"""



import os

class ClientStorage:

    def __init__(self, db_path, data):
        self.db_path = db_path
        self.data = data # словарь сообщения клиента
        self.cliendb = ObjRelMap(self.db_path)

        self.history_client = HistoryClient(self.db_path)
        self.list_clients = ListClients(self.db_path)
        self.user_model = UserModel(self.db_path)

    def add_client(self):
        try:
            field = ['id']
            username = self.data['user_id']
            add_contact = self.data['user_login']
            db_user = self.cliendb.get('UserModel', {'username': username}, field)
            db_user_add = self.cliendb.get('UserModel', {'username': add_contact}, field)
            list_data = {'username_id': db_user[0], 'client_id': db_user_add[0]}

            add = self.cliendb.get('ListClients', list_data, field)  # проверка что клиент уже добавлен

            if add:
                return False
            else:
                try:
                    self.cliendb.add('ListClients', list_data)
                    return True  # байты
                except:
                    return False  # байты
        except:
            return False

    def get_client(self):

        try:
            field = ['id']
            username = self.data['user_id']
            db_user = self.cliendb.get('UserModel', {'username': username}, field)

            join_db = self.cliendb.join([self.user_model, self.list_clients], field=['UserModel.username'],
                                        where=f'ListClients.username_id={db_user[0]}')

            return join_db  # байты
        except BaseException as e:
            return False

    def del_contact(self):
        try:
            field = ['id']
            username = self.data['user_id']
            add_contact = self.data['user_login']

            db_user = self.cliendb.get('UserModel', {'username': username}, field)
            db_user_add = self.cliendb.get('UserModel', {'username': add_contact}, field)

            list_data = {'username_id': db_user[0], 'client_id': db_user_add[0]}
            self.cliendb.delete('ListClients', list_data)

            return True
        except:
            return False

    def auth_client(self):

        try:
            field = ['id', 'password']

            username = self.data['user']['account_name']
            password = self.data['user']['password']

            auth_code = self.cliendb.get('UserModel', {'username': username}, field)
            true_auth = hmac.compare_digest(password, auth_code[1])

            if true_auth:
                update_set = {'is_active': 1}
                self.cliendb.update('UserModel', {"username": username}, update_set)

                return True

            else:
                return False

        except BaseException as e:

            return False


class FeedData(Serializer):

    def __init__(self, data, url_db):
        super().__init__(encoding="utf-8", loads=json.loads, dumps=json.dumps)
        self.data = data  # байты, пришедшие с клиента
        self.data_client = self.serializer_client(self.data)  # словарь
        self.url_db = url_db

        self.client_storage = ClientStorage(url_db, self.data_client)

        self.auth_code = None

    def analysis_data(self):
        if 'action' in self.data_client and self.data_client['action'] == 'authenticate':

            if self.client_storage.auth_client():
                self.auth_code = True
                return self.serializer_server_auth_correctly()
            else:
                return self.serializer_server_auth_warning()


        elif 'action' in self.data_client and self.data_client['action'] == 'msg':
            return self.serializer_server_message(self.data)

        elif 'action' in self.data_client and self.data_client['action'] == 'get_contacts':
            join_db = self.client_storage.get_client()
            if join_db:
                return self.serializer_server_get_client_correctly(join_db)  # байты
            else:
                return self.serializer_server_get_client_warning()

        elif 'action' in self.data_client and self.data_client['action'] == 'add_contact':
            if self.client_storage.add_client():
                return self.serializer_server_add_client_correctly()
            else:
                return self.serializer_server_add_client_warning()


        if 'action' in self.data_client and self.data_client['action'] == 'del_contact':
            if self.client_storage.del_contact():
                return self.serializer_server_delete_client_correctly()
            else:
                return self.serializer_server_delete_client_warning()

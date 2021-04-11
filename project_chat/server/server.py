from .decor_log_server import log_msg, log_auth
import selectors
from .serializer import Serializer
import json
from .db import ClientStorage, HistoryClient, ListClients, UserModel

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

class ClientStorage1():
    pass





class FeedData(Serializer):
    path = os.path.join(os.getcwd(), 'project_chat/server/company.db3')
    print(path)
    cliendb = ClientStorage(path)
    history_client = HistoryClient(path)
    list_clients = ListClients(path)
    user_model = UserModel(path)



    def __init__(self, data):
        super().__init__(encoding="utf-8", loads=json.loads, dumps=json.dumps)
        self.data = data  # байты, пришедшие с клиента

        self.data_client = self.serializer_client(self.data) #словарь

        self.history_client = HistoryClient(self.path)
        self.list_clients = ListClients(self.path)
        self.user_model = UserModel(self.path)

        self.auth_code = None

    def analysis_data(self):

        print(self.data_client, 'dict client')# словарь ответа от клиента
        if 'action' in self.data_client and self.data_client['action'] == 'authenticate':
            try:
                field = ['id']

                username = self.data_client['user']['account_name']
                password = self.data_client['user']['password']
                auth_code = self.cliendb.get('UserModel', {'username': username, 'password': password}, field)
                if auth_code:
                    self.auth_code = True
                    update_set = {'is_active': 1}
                    self.cliendb.update('UserModel', {"username": username}, update_set)

                    return self.serializer_server_auth_correctly()

                else:
                    return self.serializer_server_auth_warning()

            except BaseException as e:

                return self.serializer_server_auth_warning()



        elif 'action' in self.data_client and self.data_client['action'] == 'msg':
            return self.serializer_server_message(self.data)

        elif 'action' in self.data_client and self.data_client['action'] == 'get_contacts':
            print('get_contacts')
            field = ['id']
            username = self.data_client['user_id']
            db_user = self.cliendb.get('UserModel', {'username': username}, field)

            try:

                join_db = self.cliendb.join([self.user_model, self.list_clients], field=['UserModel.username'],
                                           where=f'ListClients.username_id={db_user[0]}')
                #[('ivan',), ('egor',)]

                return self.serializer_server_get_client_correctly(join_db) #байты
            except BaseException as e:

                print('Error ', e)
                return self.serializer_server_get_client_warning()

        elif 'action' in self.data_client and self.data_client['action'] == 'add_contact':
            field = ['id']
            username = self.data_client['user_id']
            add_contact = self.data_client['user_login']
            db_user = self.cliendb.get('UserModel', {'username': username}, field)
            db_user_add = self.cliendb.get('UserModel', {'username': add_contact}, field)
            list_data = {'username_id': db_user[0], 'client_id': db_user_add[0]}
            add = self.cliendb.get('ListClients', list_data, field)  # проверка что клиент уже добавлен

            if add:
                return self.serializer_server_add_client_warning()  # байты
            else:
                try:
                    self.cliendb.add('ListClients', list_data)
                    return self.serializer_server_add_client_correctly()  # байты

                except:
                    return self.serializer_server_add_client_warning()  # байты


        if 'action' in self.data_client and self.data_client['action'] == 'del_contact':

            try:
                field = ['id']
                username = self.data_client['user_id']
                add_contact = self.data_client['user_login']

                db_user = self.cliendb.get('UserModel', {'username': username}, field)
                db_user_add = self.cliendb.get('UserModel', {'username': add_contact}, field)

                list_data = {'username_id': db_user[0], 'client_id': db_user_add[0]}
                self.cliendb.delete('ListClients', list_data)

                return self.serializer_server_delete_client_correctly()
            except:
                return self.serializer_server_delete_client_warning()




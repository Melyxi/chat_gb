import json
import os
from .decor_log_server import log_client, log_msg


class Serializer:

    def __init__(self, encoding="utf-8", loads=json.loads, dumps=json.dumps):

        self._loads = loads
        self._dumps = dumps
        self.encoding = encoding
        self.path_auth = os.path.join(os.getcwd(), 'project_chat\\server\\db\\auth.json')
        self.path_code = os.path.join(os.getcwd(), 'project_chat\\server\\db\\code.json')
        self._LIMIT_BYTE = 640
        self.code = ' '

    def limit_byte(self, byte_str):
        while len(byte_str) < self._LIMIT_BYTE:
            byte_str += b' '
        return byte_str

    def serialize_server_authenticate_code(self, byte_string):  # проверка аунтификации
        with open(self.path_auth, encoding=self.encoding) as f:
            msg = json.load(f)
        revc_str = byte_string.decode(self.encoding)
        data = self._loads(revc_str)
        if 'action' in data and data['action'] == "authenticate":
            # print('msg', msg)
            for id in msg:
                # print(recv_msg)
                if msg[id]["account_name"] == data['user']["account_name"] and msg[id]["password"] == \
                        data['user']["password"]:
                    return '200'

            return '402'

        return '403'

    def serializer_answer_auth(self, byte_string):
        with open(self.path_code, encoding=self.encoding) as f:
            msg = json.load(f)
        code = self.serialize_server_authenticate_code(byte_string)
        result_str = self._dumps(msg[code])
        res = result_str.encode(self.encoding)

        # print(self.code, "code")
        return self.limit_byte(res)  # байты

    @log_client
    def serializer_client(self, data):
        recv_str = data.decode(self.encoding)
        recv_msg = self._loads(recv_str)
        return recv_msg  # словарь сообщения от клиента

    def serializer_server_message(self, cl_data):
        client_msg = self.serializer_client(cl_data)
        msg = client_msg['message']
        if client_msg['action'] == 'msg':
            if client_msg['message'] == 'quit':
                data = {"action": "quit"}
                result_str = self._dumps(data)
                res = result_str.encode(self.encoding)

                return self.limit_byte(res)  # байты
            else:

                data = {"response": 200, "alert": "Сообщение принято", "сообщение": msg , "action": "message"}
                result_str = self._dumps(data)
                res = result_str.encode(self.encoding)

                return self.limit_byte(res)  # байты



        else:
            with open(self.path_code, encoding=self.encoding) as f:
                msg = json.load(f)
            result_str = self._dumps(msg['403'])
            res = result_str.encode(self.encoding)

            return self.limit_byte(res)  # байты


    def serializer_server_add_client_correctly(self):
        data = {"response": "200", "message": "клиент добавлен", "action": "add_client"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты


    def serializer_server_add_client_warning(self):
        data = {"response": '404', "message": "ошибка", "action": "add_client"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

    def serializer_server_delete_client_correctly(self):
        data = {"response": "200", "message": "клиент удален", "action": "del_client"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты


    def serializer_server_delete_client_warning(self):
        data = {"response": '404', "message": "ошибка", "action": "del_client"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

    def serializer_server_get_client_correctly(self, list_client):
        print(list_client)
        clients = []
        for item in list_client:
            clients.append(item[0])

        data = {
            "response": "202",
            "alert": clients,
            "action": "get_clients"
        }

        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

    def serializer_server_get_client_warning(self):
        data = {"response": '404', "message": "ошибка", "action": "get_clients"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

    def serializer_server_auth_correctly(self):
        data = {"response": 200, "alert": "Пользователь авторизован", "action": "authenticate"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

    def serializer_server_auth_warning(self):
        data = {"response": 402, "error": "This could be 'wrong password' or 'no account with that name'", "action": "authenticate"}
        result_str = self._dumps(data)
        res = result_str.encode(self.encoding)

        return self.limit_byte(res)  # байты

# class SerializerAnswer(Serializer):
#     def __init__(self, byte_string):
#         super().__init__(byte_string, loads=json.dumps)
#
#
#     def serializer_answer_auth(self):
#         code = self.serialize_server_authenticate()
#         self.serialize_server_authenticate()
#         pass

import json
import os


class Serializer:

    def __init__(self, encoding="utf-8", loads=json.loads, dumps=json.dumps):

        self._loads = loads
        self._dumps = dumps
        self.encoding = encoding
        self.path_auth = os.path.join(os.getcwd(), 'project_chat\\server\\db\\auth.json')
        self.path_code = os.path.join(os.getcwd(), 'project_chat\\server\\db\\code.json')
        self._LIMIT_BYTE = 640

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
            print('msg', msg)
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

        return self.limit_byte(res)  # байты

    def serializer_client(self, data):
        recv_str = data.decode(self.encoding)
        recv_msg = self._loads(recv_str)
        return recv_msg  # словарь сообщения от клиента

    def serializer_server_message(self, data):
        client_msg = self.serializer_client(data)
        if client_msg['action'] == 'msg':
            if client_msg['message'] == 'quit':
                data = {"action": "quit"}
                result_str = self._dumps(data)
                res = result_str.encode(self.encoding)

                return self.limit_byte(res)  # байты
            else:
                data = {"response": 200, "alert": "Сообщение принято"}
                result_str = self._dumps(data)
                res = result_str.encode(self.encoding)

                return self.limit_byte(res)  # байты


        else:
            with open(self.path_code, encoding=self.encoding) as f:
                msg = json.load(f)
            result_str = self._dumps(msg['403'])
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

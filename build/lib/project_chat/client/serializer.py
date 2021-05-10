import json
import time

from .message import Authenticate, Message
from client.decor_log_client import log_auth_client, log_msg_client, log_server_code


class Serializer:
    def __init__(self, dumps=json.dumps, loads=json.loads, encoding="utf-8", get_time_fn=time.time):
        self._dumps = dumps
        self._encoding = encoding
        self._get_time_fn = get_time_fn
        self.loads = loads
        self._LIMIT_BYTE = 640

    def limit_byte(self, byte_str):
        while len(byte_str) < self._LIMIT_BYTE:
            byte_str += b' '
        return byte_str

    def serialize_authenticate(self, msg):
        if isinstance(msg, Authenticate):
            result_dict = {
                "action": "authenticate",
                "time": self._get_time_fn(),
                "user": {"account_name": msg.account_name, "password": msg.password, },
            }
            result_str = self._dumps(result_dict)
            res = result_str.encode(self._encoding)

            return self.limit_byte(res)  # Строка в байтах

    @log_msg_client
    def serializer_message(self, msg):
        if isinstance(msg, Message):
            result_dict = {
                "action": "msg",
                "time": self._get_time_fn(),
                "to": msg.to,
                "from": msg.from_user,
                "message": msg.message
            }

            result_str = self._dumps(result_dict)
            res = result_str.encode(self._encoding)

            return self.limit_byte(res)  # Строка в байтах

    @log_server_code
    def serializer_code(self, byte_string):
        revc_str = byte_string.decode(self._encoding)
        data = self.loads(revc_str)

        return data  # словарь сообщения от сервера

    @log_auth_client
    def serializer_code_authenticate(self, byte_string):  # код аунтификации
        return self.serializer_code(byte_string)['response']

    def serializer_get_contacts(self, username):
        result_dict = {
            "action": "get_contacts",
            "time": self._get_time_fn(),
            "user_id": username
        }
        result_str = self._dumps(result_dict)
        res = result_str.encode(self._encoding)

        return self.limit_byte(res)  # Строка в байтах

    def serializer_add_contacts(self, login, username):
        result_dict = {
            "action": "add_contact",
            "user_id": username,
            "time": self._get_time_fn(),
            "user_login": login
        }

        result_str = self._dumps(result_dict)
        res = result_str.encode(self._encoding)

        return self.limit_byte(res)  # Строка в байтах

    def serializer_del_contacts(self, login, username):
        result_dict = {
            "action": "del_contact",
            "user_id": username,
            "time": self._get_time_fn(),
            "user_login": login
        }

        result_str = self._dumps(result_dict)
        res = result_str.encode(self._encoding)

        return self.limit_byte(res)  # Строка в байтах

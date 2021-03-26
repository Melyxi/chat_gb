from .decor_log_server import log_msg , log_auth
import selectors
from .serializer import Serializer
import json

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



class FeedData(Serializer):

    def __init__(self, data):
        super().__init__(encoding="utf-8", loads=json.loads, dumps=json.dumps)
        self.data = data # байты, пришедшие с клиента


    def analysis_data(self):
        data = self.serializer_client(self.data) # словарь ответа от клиента
        if 'action' in data and data['action'] == 'authenticate':
            return self.serializer_answer_auth(self.data)

        if 'action' in data and data['action'] == 'msg':
            return self.serializer_server_message(self.data)

    def auth_user(self):

        code = self.serialize_server_authenticate_code(self.data)
        if code == '200':
            return True




if __name__ == '__main__':
    f = FeedData(b'{"code":"eewrewrew"}')
    t = f.analysis_data()
    print(t)
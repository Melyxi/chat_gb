from .decor_log_server import log_msg , log_auth
import selectors

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




from .message import Authenticate, Message


class Client:
    def __init__(self, client_socket, account_name, serializer):
        self._client_socket = client_socket
        self._account_name = account_name
        self._serializer = serializer

    def authenticate(self, password):
        msg = Authenticate(self._account_name, password)
        data = self._serializer.serialize_authenticate(msg)
        #print(data)
        self._client_socket.send(data)


    def message(self, msg, to_user):
        message = Message(self._account_name, msg, to_user)
        data = self._serializer.serializer_message(message)
        #print(data)
        self._client_socket.send(data)

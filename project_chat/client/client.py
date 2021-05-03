import hmac

from .message import Authenticate, Message



SECRET_KEY = b'HeiwrjJFEI54964fdsaKKFefkwpe'

def hashing_pass(SECRET_KEY, password):
    hash = hmac.new(SECRET_KEY, bytes(password, encoding='utf-8'), digestmod='sha256')
    digest = hash.hexdigest()
    return digest

class Client:
    def __init__(self, client_socket, account_name, serializer):
        self._client_socket = client_socket
        self.account_name = account_name
        self._serializer = serializer

    def authenticate(self, password):

        digest = hashing_pass(SECRET_KEY, password)

        msg = Authenticate(self.account_name, digest)
        data = self._serializer.serialize_authenticate(msg)
        #print(data)
        self._client_socket.send(data)


    def message(self, msg, to_user):
        message = Message(self.account_name, msg, to_user)
        data = self._serializer.serializer_message(message)
        #print(data)
        self._client_socket.send(data)

    def add_contact(self, login):

        data = self._serializer.serializer_add_contacts(login, self.account_name)
        self._client_socket.send(data)

    def del_contact(self, login):

        data = self._serializer.serializer_del_contacts(login, self.account_name)
        self._client_socket.send(data)

    def get_contacts(self):

        data = self._serializer.serializer_get_contacts(self.account_name)
        self._client_socket.send(data)


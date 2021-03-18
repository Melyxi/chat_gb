from unittest.mock import MagicMock

from project_chat.client.client import Client
from project_chat.client.message import Authenticate, Message
import pytest

def test_authenticate():
    # class MyTestSocket:
    #     def send(self, msg):
    #         self.sent_data = msg

    # class MyTestSerializer:
    #     def serialize(self, msg):
    #         self.msg = msg
    #         return b"123TEST"

    # mock_sock = MyTestSocket()
    # mock_serializer = MyTestSerializer()

    mock_sock = MagicMock()
    mock_serializer = MagicMock()
    sut = Client(mock_sock, "username", mock_serializer)

    #mock_serializer.serialize_authenticate.return_value = b"123TEST"

    sut.authenticate("password")

    # assert mock_serializer.msg == Authenticate("username", "password")
    mock_serializer.serialize_authenticate.assert_called_once_with(
        Authenticate("username", "password")
    )
    # assert mock_sock.sent_data == b"123TEST"
    #mock_sock.send.assert_called_once_with(b"123TEST")


def test_message():
    mock_sock = MagicMock()
    mock_serializer = MagicMock()
    sut = Client(mock_sock, "username", mock_serializer)
    sut.message("привет", '#room')

    mock_serializer.serializer_message.assert_called_once_with(
        Message("username", "привет", "#room")
    )




# пример
# def test_mock_example():
#     mock_fn = MagicMock()
#     mock_fn("a", 1, b"3")
#     mock_fn.assert_called_once_with("a", 1, b"3")


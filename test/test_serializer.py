import json

from project_chat.client.message import Authenticate, Message
from project_chat.client.serializer import Serializer

LIMIT_BYTE = 640

def limit_byte(byte_str):
    while len(byte_str) < LIMIT_BYTE:
        byte_str += b' '
    return byte_str

def test_serialize_authenticate():
    msg = Authenticate("igor", "123")

    expected_time = 123
    expected_msg = {
        "action": "authenticate",
        "time": expected_time,
        "user": {"account_name": msg.account_name, "password": msg.password, },
    }
    expected_data = json.dumps(expected_msg).encode("utf-8")

    expected_data = limit_byte(expected_data)

    sut = Serializer(get_time_fn=lambda: expected_time)
    assert sut.serialize_authenticate(msg) == expected_data


def test_serialize_message():
    msg = Message("igor", "привет", '#room')

    expected_time = 123
    expected_msg = {
        "action": "msg",
        "time": expected_time,
        "to": msg.to,
        "from": msg.from_user,
        "message": msg.message
    }
    expected_data = json.dumps(expected_msg).encode("utf-8")
    expected_data = limit_byte(expected_data)

    sut = Serializer(get_time_fn=lambda: expected_time)
    assert sut.serializer_message(msg) == expected_data


def test_serialize_server_auth_402():
    str_byte = json.dumps({"response": 402, "error": "no account with that name"}).encode('utf-8')

    type_dict = Serializer().serializer_code(str_byte)
    str = Serializer().serializer_code_authenticate(str_byte)

    assert type(type_dict) == dict
    assert str == 402


def test_serialize_server_auth_200():
    str_byte = json.dumps({"response": 200, "alert": "Необязательное сообщение/уведомление"}).encode('utf-8')

    type_dict = Serializer().serializer_code(str_byte)
    str = Serializer().serializer_code_authenticate(str_byte)


    assert type(type_dict) == dict
    assert str == 200


def test_serialize_server_auth_403():
    str_byte = json.dumps({
        "response": 403,
        "error": "forbidden'"
    }).encode('utf-8')

    type_dict = Serializer().serializer_code(str_byte)
    str = Serializer().serializer_code_authenticate(str_byte)

    assert type(type_dict) == dict
    assert str == 403

import pytest
from project_chat.server.serializer import Serializer
import json

LIMIT_BYTE = 640
def limit_byte(byte_str):
    while len(byte_str) < LIMIT_BYTE:
        byte_str += b' '
    return byte_str

def test_server_auth_200():
    byte_str = b'{"action": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": ' \
               b'"123"}} '

    data = Serializer().serialize_server_authenticate_code(byte_str)

    assert data == '200'

def test_server_auth_402():
    byte_str = b'{"action": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "dsfsdf", ' \
               b'"password": "fsfsf"}} '

    data = Serializer().serialize_server_authenticate_code(byte_str)

    assert data == '402'

def test_server_auth_403():
    byte_str = b'{"noaction": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "dsfsdf", ' \
               b'"password": "fsfsf"}} '

    data = Serializer().serialize_server_authenticate_code(byte_str)

    assert data == '403'


def test_server_answer_200():
    byte_str = b'{"action": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": ' \
               b'"123"}}'

    byte_str = limit_byte(byte_str)

    res = {"response": 200,"alert": "Пользователь авторизован" }
    res_byte = json.dumps(res).encode("utf-8")

    res_byte = limit_byte(res_byte)

    data = Serializer().serializer_answer_auth(byte_str)

    assert data == res_byte

def test_server_answer_402():
    byte_str = b'{"action": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": ' \
               b'"1232"}}'

    byte_str = limit_byte(byte_str)

    res = {"response": 402, "error": "This could be 'wrong password' or 'no account with that name'"}
    res_byte = json.dumps(res).encode("utf-8")

    res_byte = limit_byte(res_byte)

    data = Serializer().serializer_answer_auth(byte_str)

    assert data == res_byte


def test_server_answer_403():
    byte_str = b'{"noaction": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": ' \
               b'"1232"}}'

    byte_str = limit_byte(byte_str)

    res = {"response": 403, "error": "forbidden'"}
    res_byte = json.dumps(res).encode("utf-8")

    res_byte = limit_byte(res_byte)

    data = Serializer().serializer_answer_auth(byte_str)

    assert data == res_byte

def test_client_dict(): # словарь
    data = b'{"noaction": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": ' \
               b'"1232"}}'

    data_dict = {"noaction": "authenticate", "time": 1615116818.8811924, "user": {"account_name": "igor", "password": "1232"}}
    recv_message = Serializer().serializer_client(data)

    assert recv_message == data_dict

def test_client_answer(): # байты
    data = b'{"action": "msg", "time": 1615129600.2942805, "to": "#room", "from": "igor", "message": "fd"}'


    res = {"response": 200, "alert": "Сообщение принято"}
    res_byte = json.dumps(res).encode("utf-8")

    res_byte = limit_byte(res_byte)

    recv_message = Serializer().serializer_server_message(data)

    assert recv_message == res_byte


def test_client_answer_quit(): # байты
    data = b'{"action": "msg", "time": 1615129600.2942805, "to": "#room", "from": "igor", "message": "quit"}'


    res = {"action": "quit"}
    res_byte = json.dumps(res).encode("utf-8")

    res_byte = limit_byte(res_byte)

    recv_message = Serializer().serializer_server_message(data)

    assert recv_message == res_byte
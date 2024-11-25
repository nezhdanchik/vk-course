import threading

import pytest
from client import Client
import socket


def test_read_urls():
    client = Client('localhost', 5000, 10, 'test_urls.txt')
    assert client.urls_list == ['https://www.google.com',
                                'https://www.yandex.ru',
                                'https://www.python.org']

    with pytest.raises(FileNotFoundError):
        client = Client('localhost', 5000, 10, 'wrong_file.txt')


def test_separate():
    fake_url_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    assert Client.separate(fake_url_list, 3) == [
        '0\n1\n2',
        '3\n4\n5',
        '6\n7\n8\n9'
    ]

    assert Client.separate(fake_url_list, 5) == [
        '0\n1',
        '2\n3',
        '4\n5',
        '6\n7',
        '8\n9'
    ]

    assert Client.separate(fake_url_list, 8) == [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7\n8\n9',
    ]


server_host = '127.0.0.1'
server_port = 12345


def run_base_server(result: list):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    conn, addr = server_socket.accept()
    result[0] = (conn, addr)


def test_connect_server():
    result = [None]
    t = threading.Thread(target=run_base_server, args=(result,))
    t.start()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client.connect_server(client, server_host, server_port)
    t.join()
    assert result[0] is not None

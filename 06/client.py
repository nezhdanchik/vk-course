import os
import socket
import json
import threading
import sys


class Client:
    # pylint: disable=C0103
    def __init__(self, target_host, targe_port, M, file_urls_name):
        self.target_host = target_host
        self.target_port = targe_port
        self.M = M  # pylint: disable=C0103
        self.file_urls_path = file_urls_name
        self.urls_list = self.read_urls()
        print(self.urls_list)

    def read_urls(self):
        file_path = os.path.join(os.path.dirname(__file__), self.file_urls_path)
        with open(file_path, encoding='utf-8') as file:
            return [i.strip() for i in file]

    @staticmethod
    def connect_server(socket_obj, host, port):
        socket_obj.connect((host, port))

    @staticmethod
    def send_message(text: str, socket_obj):
        socket_obj.send(text.encode())

    @staticmethod
    def get_response(socket_obj) -> str:
        return socket_obj.recv(2 ** 20).decode()

    def worker(self, text):
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_server(new_socket, self.target_host, self.target_port)
        self.send_message(text, new_socket)
        response = self.get_response(new_socket)
        processed = json.loads(response)
        print(json.dumps(processed, indent=4))

    @staticmethod
    # pylint: disable=C0103
    def separate(urls_list, M) -> list[str]:
        part_size = len(urls_list) // M
        parts = [
            urls_list[part_size * i:  part_size * (i + 1)]
            for i in range(M)
        ]
        remains_count = len(urls_list) % M
        remains = urls_list[-remains_count:] if remains_count != 0 else []
        parts[-1] += remains
        return ['\n'.join(p) for p in parts]

    def run(self):
        parts = self.separate(self.urls_list, self.M)
        threads = [
            threading.Thread(target=self.worker, args=(p,))
            for p in parts
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()


if __name__ == '__main__':
    # python client.py 10 urls.txt
    M_arg = int(sys.argv[1])
    file_name = sys.argv[2]
    c = Client('127.0.0.1', 12345, M_arg, file_name)
    c.run()

from collections import Counter
from collections.abc import Iterable
from urllib.request import urlopen
from queue import Queue
from json import dumps
import threading
import socket
import sys


class Server:
    def __init__(self, host: str, port: int, workers=10, k=10):
        self.host = host
        self.port = port
        self.workers = workers
        self.k = k  # количество самых частых слов
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))

    def __str__(self):
        return f'{self.host}:{self.port}'

    def find_most_common_words(self, url: str, k: int, case_sensitive=False):
        """
        :param url: url, по которому происходит поиск
        :param k: количество самых частых слов
        :param case_sensitive: учитывать регистр
        :return: словарь частотности содержания url
        """

        try:
            response = urlopen(url)
        except Exception as err:
            print(f'can\'t process url {url}; {err=}')
            return
        content = response.read().decode()

        # удаляем все символы, не являющиеся буквой
        for i in set(content):
            if not i.isalpha():
                content = content.replace(i, ' ')

        # если не нужно учитывать регистр
        if not case_sensitive:
            content = content.lower()

        content_list = content.split()
        return dict(Counter(content_list).most_common(k))

    def url_worker(self, urs_queue: Queue[str], k: int, result: dict,
                   connection: socket.socket,
                   case_sensitive=False):
        while True:
            url = urs_queue.get()
            if not url:
                urs_queue.put(url)
                return
            result[url] = self.find_most_common_words(url, k, case_sensitive)
            print(f'обработано {len(result)} url\'ов для клиента {connection.getpeername()}')

    def process_urls(self, urls: Iterable[str], connection: socket.socket) -> str:
        """
        :param connection: объект соединения с клиентом
        :param urls: url'ы, для которых нужно получить словарь частотности
        :return: json строка вида key=url value={'word1': n, 'word2': m}
        """
        urls_queue = Queue()
        for url in urls:
            urls_queue.put(url)
        # флаг для завершения
        urls_queue.put(None)

        result = dict()
        working_threads = [
            threading.Thread(target=self.url_worker,
                             args=(urls_queue, self.k, result, connection),
                             kwargs={'case_sensitive': False})
            for _ in range(self.workers)
        ]

        for wt in working_threads:
            wt.start()
        for wt in working_threads:
            wt.join()

        return dumps(result)

    def process_connection(self, conn, addr):
        print(f"Connected with client {addr}")
        with conn:
            while True:
                data = conn.recv(2 ** 20)
                if not data:
                    break
                decoded_data = data.decode()
                urls = decoded_data.split('\n')
                result = self.process_urls(urls, conn)
                conn.send(result.encode())
            print(f'End connection with client {addr}')

    def run(self):
        print(f'server {self} started')
        while True:
            self.socket.listen()
            conn, addr = self.socket.accept()
            threading.Thread(target=self.process_connection,
                             args=(conn, addr)).start()

    def __del__(self):
        print(f'server {self} stopped')
        self.socket.close()

if __name__ == '__main__':
    # python server.py -w 10 -k 7
    workers = sys.argv.index('-w') + 1
    k = sys.argv.index('-k') + 1
    s = Server('127.0.0.1', 12345, workers=workers, k=k)
    s.run()

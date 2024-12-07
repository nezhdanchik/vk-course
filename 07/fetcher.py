import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os


class URLDispatcher:
    def __init__(self, count, file_name):
        self.count = count
        self.file_name = file_name
        self.sem = asyncio.Semaphore(count)
        self.url_generator = self.get_url_generator()

    def get_url_generator(self):
        file_path = os.path.join(os.path.dirname(__file__), self.file_name)
        with open(file_path) as file:
            for url in file:
                yield url.strip()

    async def get_title(self, url: str, session):
        async with self.sem:
            async with session.get(url) as response:
                content = await response.read()
                soup = BeautifulSoup(content, 'html.parser')
                return soup.title.text

    async def fetch_all(self):
        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(
                *[self.get_title(url, session) for url in self.url_generator])
            return result

    async def main(self):
        return await self.fetch_all()


class ParseURLDispatcherArgs:
    @staticmethod
    def parse(string: str | None = None):
        parser = argparse.ArgumentParser()
        parser.add_argument('count', nargs='?', type=int)
        parser.add_argument('-c', type=int)
        parser.add_argument('file', type=str)
        try:
            if string:
                args = parser.parse_args(string.split())
            else:
                args = parser.parse_args()
        except SystemExit:
            raise ValueError('Неправильные аргументы при запуске')

        count_arg = args.c if args.c else args.count
        file_arg = args.file
        if not count_arg or not file_arg:
            raise ValueError('Неправильные аргументы при запуске')
        print(count_arg, file_arg)
        return count_arg, file_arg


if __name__ == '__main__':
    # python fetcher.py -c 10 urls.txt | python fetcher.py 10 urls.txt
    u = URLDispatcher(*ParseURLDispatcherArgs.parse())
    print(asyncio.run(u.main()))

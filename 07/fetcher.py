import os
import sys
import asyncio
import aiohttp


class URLDispatcher:
    def __init__(self, part_size, file_name):
        self.part_size = part_size
        self.file_name = file_name
        self.parts = self.create_parts(self.read_urls())

    def create_parts(self, urls):
        parts = []
        current = []
        for url in urls:
            current.append(url)
            if len(current) == self.part_size:
                parts.append(current)
                current = []
        if current:
            parts.append(current)
        return parts

    def read_urls(self):
        file_path = os.path.join(os.path.dirname(__file__), self.file_name)
        with open(file_path) as file:
            return [i.strip() for i in file]

    @staticmethod
    async def fetch_url(url, session):
        async with session.get(url) as response:
            return response.status

    async def main(self):
        async with aiohttp.ClientSession() as session:
            coroutines = [self.fetch_url(url, session) for url in self.parts]
            result = await asyncio.gather(*coroutines)
            print(result)


if __name__ == '__main__':
    # python fetcher.py -c 10 urls.txt | python fetcher.py 10 urls.txt
    if '-c' in sys.argv:
        part_size_arg = sys.argv.index('-c') + 1
    else:
        part_size_arg = sys.argv[2]
    file_name_arg = sys.argv[-1]
    dispatcher = URLDispatcher(part_size_arg, file_name_arg)
    asyncio.run(dispatcher.main())

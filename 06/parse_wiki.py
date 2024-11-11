from bs4 import BeautifulSoup
import requests


url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
base = 'https://en.wikipedia.org/'

def parse_urls(size=100, skip=30):
    urls = set()
    response = requests.get(url)
    page = BeautifulSoup(response.content, features='html.parser')
    for ind, tag_a in enumerate(page.find_all('a')):
        link = tag_a.get('href')
        if link and link.startswith('/wiki/') and '#' not in link:
            urls.add(f'{base}{link}')
        if len(urls) == size + skip:
            return list(urls)[skip:]


with open('urls.txt', 'w') as file:
    file.write('\n'.join(parse_urls()))

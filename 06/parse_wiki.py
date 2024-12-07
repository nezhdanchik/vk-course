import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Python_(programming_language)"
BASE = "https://en.wikipedia.org/"


def parse_urls(size=100, skip=30):
    urls = set()
    response = requests.get(URL, timeout=10)
    page = BeautifulSoup(response.content, features="html.parser")
    for tag_a in page.find_all("a"):
        link = tag_a.get("href")
        if link and link.startswith("/wiki/") and "#" not in link:
            urls.add(f"{BASE}{link}")
        if len(urls) == size + skip:
            return list(urls)[skip:]
    return None


with open("urls.txt", "w", encoding='utf-8') as file:
    file.write("\n".join(parse_urls()))

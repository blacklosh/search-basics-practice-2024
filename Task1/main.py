import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

filenum = 1
limit = 102


def crawl(start_url, folder):
    visited = set()

    def add_to_index(url, filename):
        with open(indexfile, "a") as index:
            index.write(f"{filename} {url}\n")

    def save_html(url, soup):
        global filenum
        global limit

        if limit < 1:
            sys.exit()
        else:
            limit = limit - 1

        filename = os.path.join(folder, f"{filenum}.html")
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f_out:
            f_out.write(soup.prettify())

        add_to_index(url, filename)
        filenum = filenum + 1

    def get_links(url):
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        save_html(url, soup)
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('#'):
                full_url = urljoin(url, href)
                if full_url not in visited:
                    visited.add(full_url)
                    yield full_url

    def crawl_recursive(url):
        for link in get_links(url):
            if link.startswith(start_url):
                print(f"Crawling: {link}")
                crawl_recursive(link)

    crawl_recursive(start_url)


start_url = 'https://info.cern.ch/hypertext/WWW/'
folder = 'c:/cfg/crawl5/'
indexfile = folder + 'index.txt'

crawl(start_url, folder)
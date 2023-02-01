from pprint import pprint

import requests
from bs4 import BeautifulSoup

URL = "https://www.securitylab.ru/news/"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="article-card inline-card")
    news = list()
    for item in items:
        new = {
            "title": item.find("h2", class_="article-card-title").string,
            "description": item.find("p").string,
            "date": item.find("time").getText()
        }
        news.append(new)
    return news


def parser():
    html = get_html(URL)
    if html.status_code == "200":
        news = []
        for i in range(1, 2):
            html = get_html(f"{URL}page/{i}/")
            new = get_data(html.text)
            news.extend(new)
        return news
    else:
        raise Exception("Error in parser!")

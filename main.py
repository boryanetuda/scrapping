import requests
import bs4
from fake_headers import Headers
from pprint import pprint

url_0 = 'https://habr.com'
url = 'https://habr.com/ru/all/'

heads = Headers(os='mac', headers=True).generate()
KEYWORDS = ['дизайн', 'фото', 'web', 'Python']


class Finder:

    items = []

    def __init__(self, text):
        self.text = text

    def find_match(self, article):
        for txt in self.text:
            for word in KEYWORDS:
                if word.lower() in txt.lower():
                    href = article.find(class_='tm-article-snippet__title-link').attrs['href']
                    art_name = article.find('h2').find('span').text
                    datetime = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
                    link = url_0+href
                    result = f'{datetime}, {art_name}, {link}'
                    Finder.items.append(result)


def start():
    resp = requests.get(url, headers=heads)
    resp.raise_for_status()
    text = resp.text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    for article in articles:
        arts = article.find_all(class_='tm-article-snippet__title-link')
        arts = set(art.text.strip() for art in arts)
        arts_find = Finder(arts)
        arts_find.find_match(article)
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = set(hub.text for hub in hubs)
        hubs_find = Finder(hubs)
        hubs_find.find_match(article)
        mains = article.find_all(class_='article-formatted-body')
        mains = set(main.text for main in mains)
        main_find = Finder(mains)
        main_find.find_match(article)


def final():
    li = []
    [li.append(x) for x in Finder.items if x not in li]
    pprint(li)


if __name__ == '__main__':
    start()
    final()
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random
import string

def get(id, page):
    url = f'https://asked.kr/query.php?query=1&page={page}&id={id}'
    response = requests.get(url)
    return response.content.decode()

def parse(soup):
    cards = soup.findAll('div', {'class': 'card'})
    parsed_cards = []

    SUCCESS, FAILURE = 0, 0

    for card in cards:
        try:
            parsed_cards.append({
                'name': card.find('span', {'class': 'ask_name'}).text,
                'ask': card.find('div', {'class': 'card_ask'}).text,
                'time': card.find('div', {'class': 'card_time'}).text,
                'answer': card.find('div', {'class': 'card_answer'}).text,
            })
            SUCCESS += 1
        except AttributeError:
            FAILURE += 1

    print('parsing fin, SUCCESS:', SUCCESS, '| FAILURE:', FAILURE)

    return parsed_cards

lista = []

def adddata(data):
    global lista
    lista += data

letters = string.ascii_letters

def save_as_file(anything, name):
    if name == None:
        name = ''.join(random.choice(letters) for i in range(10)) + '.txt'
    print('saved as ' + name)
    with open(name, 'w', encoding='utf-8') as f:
        f.write(str(anything))

class Crawler:
    def __init__(self, id=None, page=0):
        self.id = id
        self.page = page

        self.save = False
        self.save_name = None

    def save_on(self, name=None):
        self.save = True
        self.save_name = name

    def crawl(self):
        print('id :', self.id, '| page :', self.page)
        print('start crawling...')
        start_crawl(self.id, self.page, save=self.save, save_name=self.save_name)

def start_crawl(id, page, save, save_name):
    for i in range(page):
        print(f'trying {id} -> {i}')
        soup = BeautifulSoup(get(id, i), 'html.parser')
        parsed = parse(soup)
        adddata(parsed)
        if save:
            save_as_file(lista, save_name)
    print('------->> crawling fin')
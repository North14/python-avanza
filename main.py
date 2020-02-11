#!/bin/env python3

import requests
import yaml
from tabulate import tabulate
import bs4


def request(url):
    r = requests.get(url)
    return r.text

def parse_class(r_html, options):
    soup = bs4.BeautifulSoup(r_html, features='lxml')
    class_text = []

    shortcode = soup.find('title').get_text().split('-', 1)[0]
    class_text.append(shortcode)

    for option in options:
        class_text.append(soup.find('span', attrs={'class': option}).get_text())
    return class_text

def list_urls(data):
    url = []        
    for types in ('stocks', 'certs'):
        for x in data[types]:
            if types == 'stocks':
                url.append(BASE_STOCK_URL + x)
            elif types == 'certs':
                url.append(BASE_CERT_URL + x)
    return url

def open_yml():
    with open(YML_FILE, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
    return data

def main():
    data = open_yml()
    urls = list_urls(data)
    tabulate_list = [['shortcode']] 
    for option in data['options']:
        tabulate_list[0].append(option)
    for url in urls:
        tabulate_list.append(parse_class(request(url), data['options']))
    print(tabulate(tabulate_list, headers='firstrow'))

if __name__ == "__main__":
    global BASE_STOCK_URL, BASE_CERT_URL, FILE
    YML_FILE = "data.yml"
    BASE_STOCK_URL = "https://www.avanza.se/aktier/om-aktien.html/"
    BASE_CERT_URL = "https://www.avanza.se/borshandlade-produkter/certifikat-torg/om-certifikatet.html/"
    main()

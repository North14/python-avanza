#!/bin/env python3

import requests
import yaml
from tabulate import tabulate
import bs4


def request(url):
    """ dl url """
    r = requests.get(url)
    return r.text

def parse_class(r_html, options):
    """
    parses avanza html for data
    """
    soup = bs4.BeautifulSoup(r_html, features='lxml')
    class_text = []

    shortcode = soup.find('title').get_text().split('-', 1)[0]
    class_text.append(shortcode)

    for option in options:
        class_text.append(soup.find('span', attrs={'class': option}).get_text())
    return class_text

def list_urls(data):
    """
    adds avanza url to data
    """
    for types in ('stocks', 'certs'):
        for x in data[types]:
            x['url'] = (BASE_STOCK_URL + x['name'])
    return data

def open_yml():
    """
    imports the yml data file
    """
    with open(YML_FILE, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
    return data

def main():
    data = list_urls(open_yml())
    tabulate_list = [['shortcode', 'paidPrice', 'profit']] 
    for option in data['options'][::-1]:
        tabulate_list[0].insert(1, option)
    for types in ('stocks', 'certs'):
        for x in data[types]:
            if ('price' in x) and ('amount' in x):
                list1 = parse_class(request(x['url']), data['options'])
                totalprice = round(x['price'] * x['amount'], 2)
                profit = round(((float(list1[2].replace(',', '.')) * x['amount']) - totalprice), 2)
                list1.extend([totalprice, profit])
            else:
                list1 = parse_class(request(x['url']), data['options'])
                list1.extend(['-', '-'])
            tabulate_list.append(list1)

    print(tabulate(tabulate_list, headers='firstrow'))

if __name__ == "__main__":
    global BASE_STOCK_URL, BASE_CERT_URL, FILE
    YML_FILE = "data.yml"
    BASE_STOCK_URL = "https://www.avanza.se/aktier/om-aktien.html/"
    BASE_CERT_URL = "https://www.avanza.se/borshandlade-produkter/certifikat-torg/om-certifikatet.html/"
    main()

#!/bin/env python3

import requests
import yaml
from tabulate import tabulate
import bs4


def request(url):
    r = requests.get(url)
    return r.text

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
    with open(FILE, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
    return data

def main():
    data = open_yml()
    urls = list_urls(data)
    print(urls)

if __name__ == "__main__":
    global BASE_STOCK_URL, BASE_CERT_URL, FILE
    FILE = "data.yml"
    BASE_STOCK_URL = "https://www.avanza.se/aktier/om-aktien.html/"
    BASE_CERT_URL = "https://www.avanza.se/borshandlade-produkter/certifikat-torg/om-certifikatet.html/"
    main()

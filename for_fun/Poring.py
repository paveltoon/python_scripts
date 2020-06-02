import requests
import json
import urllib.parse
from classes_try import Car

niles = Car('BMW', 'E46', 2001, "+5 Nile's Bracelet")
print(niles.get_status())


def getItemPrices(item_name):
    items_url = f'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory' \
                f'=&q={urllib.parse.quote(item_name)}'
    res = requests.get(items_url)
    items_json = json.loads(res.text)
    items_list = []
    for item in items_json:
        nile = {'name': item['name'], 'price': item['lastRecord']['price']}
        items_list.append(nile)
    for item in sorted(items_list, key=lambda i: i['price']):
        print(item['name'], item['price'])


getItemPrices("Nile's Bracelet")

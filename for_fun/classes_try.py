class Car:
    import requests
    import json
    import urllib.parse

    def __init__(self, name, model, year, item_name):
        self.name = name
        self.model = model
        self.year = year
        self.item_name = item_name

    def start(self):
        print(f'Двигатель {self.name} {self.model} запущен.')

    def stop(self):
        print(f'Двигатель {self.name} заглушен')

    def get_status(self):
        res = self.requests.get(f'https://poring.world/api/search?order=popularity&rarity=&inStock=1&modified=&category=&endCategory=&q={self.urllib.parse.quote(self.item_name)}')
        items_json = self.json.loads(res.text)
        items_list = []
        for item in items_json:
            nile = {'name': item['name'], 'price': item['lastRecord']['price']}
            items_list.append(nile)
        return sorted(items_list, key=lambda i: i['price'])

import requests
response = requests.get('https://poring.world/api/search?')
print(response.text)

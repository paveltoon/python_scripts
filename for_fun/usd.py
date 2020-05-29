import requests
import json
req = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
parse = json.loads(req.text)
print(parse['rates']['RUB'])
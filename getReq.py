import requests
urls = {
    "http://10.10.80.20/api/statuses/",
    "http://10.10.80.21/api/statuses/"
}

for url in urls:
    res = requests.get(url)
    print(res.text)
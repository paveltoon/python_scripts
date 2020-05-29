import lxml.html
import requests

url = 'https://www.afisha.ru/msk/schedule_concert/'
api = requests.get(url)
dom_tree = lxml.html.document_fromstring(api.text)

artist_name = dom_tree.xpath('//*[@id="widget-content"]//a[@class="_1F19s"]/text()')
concert_place = dom_tree.xpath('//*[@id="widget-content"]//div[@class="_1Jo7v"]/span/a/text()')
concert_date = dom_tree.xpath('//*[@id="widget-content"]//div[@class="_1Jo7v"]/text()[2]')
try:
    for i in range(len(artist_name)):
        print(artist_name[i], concert_place[i], concert_date[i], sep='\n', end='\n\n')
except Exception as er:
    print(er)

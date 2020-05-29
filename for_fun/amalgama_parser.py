import lxml.html
import requests


def parse(url):
    api = requests.get(url)
    tree = lxml.html.document_fromstring(api.text)
    original_text_tree = tree.xpath('//*[@id="click_area"]/*[@class="string_container"]//*[@class="original"]/text()')
    translate_text_tree = tree.xpath('//*[@id="click_area"]/*[@class="string_container"]//*[@class="translate"]/text()')
    for i in range(len(original_text_tree)):
        print(original_text_tree[i], translate_text_tree[i])


parse('https://www.amalgama-lab.com/songs/l/little_big/uno.html')

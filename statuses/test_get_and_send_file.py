from requests import request
import json
import quopri
from io import BytesIO

get_url = "http://10.10.80.54:8080/api/fs/file/"
send_url = "http://10.10.80.20/api/fs/file"


def get_file(_id):
    _response = request("GET", get_url + str(_id), stream=True)
    return _response


def send_file(_name, _file):
    payload = {
        'name': _name
    }
    files = {
        'file': _file,
    }
    _response = request("POST", send_url, data=payload, files=files)
    return json.loads(_response.text)


file = get_file("56f662daa78eddb3ffe1650f")
filename = quopri.decodestring(file.headers['content-disposition'].replace('%', '=').split('filename=')[1]).decode('utf-8')
file_in_bytes = BytesIO(file.content)
print(filename)
# response = send_file(filename, file_in_bytes)
# print(response)

from requests import request
import json

host = "10.10.80.54:8080"


def send_file(_file):
    url = f"http://{host}/api/fs/file"
    payload = {
        'name': _file
    }
    files = {
        'file': open(_file, 'rb'),
    }
    response = request("POST", url, data=payload, files=files)
    return json.loads(response.text)


sendFile = send_file("фото2.jpg")
print(sendFile)

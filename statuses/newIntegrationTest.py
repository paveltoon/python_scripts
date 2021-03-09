from requests import request
import json

host = "10.10.80.54:8080"
statusCode = "10"


def create_status(claim_id):
    url = f"http://{host}/api/statuses/"
    headers = {
        'Content-Type': 'application/json'
    }
    new_status = {
        "claimId": str(claim_id),
        "statusCode": statusCode,
        "senderCode": "906090",
        "senderName": "AISLOD",
        "createState": "INIT"
    }
    response = request("POST", url=url, headers=headers, data=json.dumps(new_status))
    resJson = json.loads(response.text.encode('utf8'))
    return resJson["id"]


def create_doc(owner_id, owner_type, title, _file_metadata):
    url = f"http://{host}/api/docs"
    headers = {
        'Content-Type': 'application/json'
    }
    docInit = {
        "ownerId": str(owner_id),
        "ownerType": str(owner_type),
        "type": {
            "title": title,
            "required": False
        },
        "fileMetadata": _file_metadata,
        "title": title
    }
    response = request("POST", url=url, headers=headers, data=json.dumps(docInit))
    resJson = json.loads(response.text.encode('utf8'))
    return resJson["id"]


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


def update_status(status_id, claim_id):
    url = f"http://{host}/api/statuses/"
    headers = {
        'Content-Type': 'application/json'
    }
    upd_status = {
        "id": str(status_id),
        "claimId": str(claim_id),
        "statusCode": statusCode,
        "senderCode": "906090",
        "senderName": "AISLOD",
        "createState": "COMPLETED",
    }
    response = request("POST", url=url, headers=headers, data=json.dumps(upd_status))
    resJson = json.loads(response.text.encode('utf8'))
    return resJson




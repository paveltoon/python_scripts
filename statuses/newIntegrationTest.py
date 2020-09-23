from rldd import rldd2
from requests import request
import json

host = "10.10.80.20"
statusCode = "10"

db = rldd2.DEV_connect()
claims = db.claims.find({
    "customClaimNumber": {
        "$in": [
            "P001-4736138748-23267568"
        ]
    }
})


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


for claim in claims:
    claimId = claim["_id"]
    statusId = create_status(claimId)

    sendFile1 = send_file("P001-4736138748-23267568_Zhaloba.odt")
    docId = create_doc(statusId, "STATUS",  "P001-4736138748-23267568_Zhaloba.odt", sendFile1)
    sendFile2 = send_file("Snimok+ekrana+ot+2020-09-09+15-00-42.png")
    docId2 = create_doc(statusId, "STATUS", "Snimok+ekrana+ot+2020-09-09+15-00-42.png", sendFile2)
    sendFile3 = send_file("Reshenie_ob_otka_taxi_duplicate_OOO_OOO__RUBES.odt")
    docId3 = create_doc(statusId, "STATUS", "Reshenie_ob_otka_taxi_duplicate_OOO_OOO__RUBES.odt", sendFile3)

    updateStatus = update_status(statusId, claimId)
    print(updateStatus)

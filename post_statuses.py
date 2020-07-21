from rldd import rldd2
from user import rldd_user
from bson import ObjectId
import requests
import json
url = 'http://10.10.80.54:8080/api/statuses'
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({"_id": {"$in": [
    ObjectId("5f05c14922e5c600011f3f04"),
    ObjectId("5f05c3ea22e5c600011f6887"),
    ObjectId("5f05c62622e5c600011f88be"),
    ObjectId("5f05e24622e5c600013bb386"),
    ObjectId("5f05e67c22e5c600013bd2e9"),
    ObjectId("5f05e70e22e5c600013bd57c"),
    ObjectId("5f05f5e922e5c600013c418f")
]}})
for claim in claims:
    _id = claim["_id"]
    status = {
        "claimId": str(_id),
        "statusCode": "5",
        "createBy": "rldd2",
        "comment": "Просим вас заново подать заявление и необходимые для предоставления услуги документы.",
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(status), headers=headers)
    print(response.text.encode('utf8'))

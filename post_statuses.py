from rldd import rldd2
from user import rldd_user
from bson import ObjectId
import requests
import json
url = 'http://10.10.80.54:8080/api/statuses'
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({"_id": {"$in": [
    ObjectId("5f03514422e5c600010e2ef5"),
    ObjectId("5f03516422e5c600010e2f4c"),
    ObjectId("5f03520e22e5c600010e3408"),
    ObjectId("5f04515622e5c6000113a9c5"),
    ObjectId("5f04afa522e5c60001181a66"),
    ObjectId("5f057b1e22e5c600011b2e94"),
    ObjectId("5f057b6322e5c600011b30ca"),
    ObjectId("5f057bab22e5c600011b343a")
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

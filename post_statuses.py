from rldd import rldd2
from user import rldd_user
import requests
import json

url = 'http://10.10.80.54:8080/api/statuses'
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({"customClaimNumber": {"$in": [
    "M504-4983323246-36368946"
]}})

# claims = db['claims'].find(
#     {"senderCode": {'$regex': '^50.*'}, "service.srguServiceId": "5000000000181746269", "currStatus.statusCode": "2"})
for claim in claims:
    _id = claim["_id"]
    status = {
        "claimId": str(_id),
        "statusCode": "40",
        "createBy": "rldd2",
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(status), headers=headers)
    print(response.text.encode('utf8'))

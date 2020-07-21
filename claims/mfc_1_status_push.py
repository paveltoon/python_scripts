import json

from rldd import rldd2
from user import rldd_user
import requests

claims_list = [
    "mfc-mfc F503-5903825-0557000323",
    "mfc-mfc F503-1285485-0087000058",
    "mfc-mfc F503-9812395-0087000059",
    "mfc-mfc F503-7484413-0387001365",
    "mfc-mfc F503-2045910-2087000009",
    "mfc-mfc F503-2829749-0978000868"
]

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
result_file = open("ids.txt", "w+")
for elem in claims_list:
    space_index = elem.rfind(" ")
    ccn = elem[space_index + 1:]
    claim = db["claims"].find_one({"customClaimNumber": ccn})
    if claim is not None:
        result_file.write(f"{claim['_id']}\n")
        url = "http://10.10.80.54:8080/api/statuses/"
        payload = {
            "claimId": str(claim["_id"]),
            "statusCode": "1",
            "createBy": "rldd2",
            "comment": "Статус создан автоматически через РЛДД, для корректного закрытия заявки",
            "lastModifiedBy": "rldd2",
            "createState": "COMPLETED"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url=url, headers=headers, data=json.dumps(payload))
        print(res.text.encode('utf8'))
    else:
        print(ccn)
result_file.close()
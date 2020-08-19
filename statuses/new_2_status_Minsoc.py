from rldd import rldd2
from user import rldd_user
import json
import requests
import os.path

# Variables
status = "2"
desktop = os.path.expanduser('~/Desktop')
result_file = open(f'{desktop}\\send2Status.log', 'w+')
url = "http://10.10.80.54:8080/api/statuses/"
headers = {
    'Content-type': 'application/json'
}

# Connect
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find(
    {"service.srguServiceId": "5000000000181746269", "service.srguServicePassportId": "5000000010000000897",
     "currStatus.statusCode": "2", "consultation": {"$ne": True}, "senderCode": {"$ne": "IPGU01001"}})
for claim in claims:
    _id = claim["_id"]
    ccn = claim["customClaimNumber"]
    req_body = {
        "claimId": str(_id),
        "comment": "Статус создан автоматически через РЛДД, для корректного закрытия заявки",
        "statusCode": status,
        "createBy": "rldd2",
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED"
    }
    response = requests.request("POST", url=url, data=json.dumps(req_body), headers=headers)
    print(response.text.encode('utf-8'))
    if 200 <= int(response.status_code) <= 300:
        result_file.write(f'{ccn} was added {status} status.\n')
result_file.close()

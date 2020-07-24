import json
from rldd import rldd2
from datetime import timedelta
import requests
from user import rldd_user


def sendStatus(_claim_id, _status, _status_date):
    url = "http://10.10.80.54:8080/api/statuses"
    statusElem = {
        "claimId": str(_claim_id),
        "statusCode": str(_status),
        "createBy": "rldd2",
        "statusDate": _status_date.isoformat(),
        "comment": "Статус создан автоматически через РЛДД, для корректного закрытия заявки, в рамках тикета 0000-000821011",
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.post(url, data=json.dumps(statusElem), headers=headers)


db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({
    "customClaimNumber": {
        '$in': [
            "B001-7946460468-33971954",
            "B001-2855015596-34067728",
            "B001-0441652276-34251215",
            "B001-6984992670-34148440"
        ]
    }
}
)
for claim in claims:
    claimId = claim['_id']
    statuses = db['claims_status'].find({"claimId": str(claimId)})
    for status in statuses:
        if status['statusCode'] == "6":
            statusDate = status['statusDate']
            firstStatusDate = statusDate + timedelta(milliseconds=120)
            secondStatusDate = statusDate + timedelta(milliseconds=240)
            firstStatus = sendStatus(claimId, 3, firstStatusDate)
            secondStatus = sendStatus(claimId, 24, secondStatusDate)
            print(firstStatus.text.encode('utf-8'))
            print(secondStatus.text.encode('utf-8'))

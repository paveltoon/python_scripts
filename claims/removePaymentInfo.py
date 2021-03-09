import json

import requests
from deadlines.deadline_functions import setDeadlineToOneDay
from rldd.client import Client
from rldd.config import PROD, DEV

db = Client(PROD).connect()


def postStatus(body):
    url = 'http://10.10.80.54:8080/api/statuses/'

    headers = {
        'Content-Type': 'application/json'
    }

    del body["_id"]
    del body["statusDate"]
    del body["createDate"]
    del body["lastModified"]
    del body["_class"]

    requests.request("POST", url=url, headers=headers, data=json.dumps(body))


query = {
    "service.srguServicePassportId": {
        "$in": [
            "5000000010000000897",
            "5000000000185430600",
            "5000000000186973891"
        ]
    },
    "claimCreate": {
        "$gte": Client.ISODate("2018-12-31T21:00:00.000+0000"),
        "$lte": Client.ISODate("2019-12-31T21:00:00.000+0000")
    },
    "currStatus.statusCode": {
        "$in": ["77", "78"]}}

claims = db["claims"].find(query)
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    upd = db["claims"].update_one({
        "_id": claimId
    }, {
        "$unset": {
            "service.paymentInfo": ""
        }
    })
    status = db["claims_status"].find_one({"claimId": str(claimId), "statusCode": "24"})
    if status:
        postStatus(status)
    setDeadlineToOneDay(query)
    db["claims"].update_one({"_id": claimId}, {
        "$pull": {
            "fields.sequenceValue": {
                "stringId": {
                    "$in": [
                        "sendAttachWithResultStatus",
                        "additionalPaymentRequired",
                        "paymentType"
                    ]
                }
            }
        }
    })
    print(f"Claim: {ccn}, progress: {upd.modified_count} / {upd.matched_count}")

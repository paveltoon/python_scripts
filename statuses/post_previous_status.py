import pymongo
import datetime
import requests
from bson import ObjectId

from rldd.client import Client
from rldd import config
import json


def post_full_status(status_dict):
    body = status_dict
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.post(url='http://10.10.80.54:8080/api/statuses', data=json.dumps(body), headers=headers)


projection = {
    "customClaimNumber": 1,
    "_id": 1,
    "currStatus": 1
}
query = {"activationDate": {'$gte': Client.ISODate("2020-01-01T08:40:43.439+0000"),
                            '$lte': Client.ISODate("2020-08-29T08:40:43.439+0000")},
         "consultation": False,
         "service.srguServicePassportId": "5000000000193224739",
         "currStatus.senderCode": "RGIS05001"
         }
db = Client(config.PROD).connect()
claims = db["claims"].find(query, projection)
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    statuses = list(db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.DESCENDING))
    for i in range(len(statuses)):
        try:
            status = statuses[i]
            if status["statusCode"] == "6" and status["senderCode"] == "RGIS05001":
                new_status = statuses[i + 1]

                del new_status["_id"]
                del new_status["statusDate"]
                del new_status["createDate"]
                del new_status["lastModified"]
                del new_status["_class"]

                response = post_full_status(new_status)
                print(response.text.encode('utf-8'))
                continue
        except IndexError as ie:
            print(claimId, ie)

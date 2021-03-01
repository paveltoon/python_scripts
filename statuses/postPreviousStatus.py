import json

import pymongo
import requests
from bson import ObjectId

from rldd.client import Client
from rldd import config


def post_full_status(status_dict):
    body = status_dict
    headers = {
        'Content-Type': 'application/json'
    }
    return requests.post(url='http://10.10.80.54:8080/api/statuses', data=json.dumps(body), headers=headers)


db = Client(config.PROD).connect()
claims = db["claims"].find({"_id": {
    "$in": [
        ObjectId("5daf15a78a19c400016f2a6d"),
        ObjectId("5dea323eb8b4270001b3e949"),
        ObjectId("5cb726155ea23cd61a71623f"),
        ObjectId("5c9c80425ea28667e3d4c193")
    ]
}})

for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    statuses = list(db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.ASCENDING))
    new_status = statuses[len(statuses) - 2]
    del new_status["_id"]
    del new_status["statusDate"]
    del new_status["createDate"]
    del new_status["lastModified"]
    del new_status["_class"]
    response = post_full_status(new_status)
    print(response.text.encode('utf-8'))

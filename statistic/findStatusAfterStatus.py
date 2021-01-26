import pymongo

from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({
    "service.srguServicePassportId": "5000000000166988901",
    "activationDate": {
        '$gte': Client.ISODate("2019-12-31T21:00:00.000+0000"),
        '$lte': Client.ISODate("2020-12-07T21:00:00.000+0000")
    }
})

for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    statuses = list(db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.ASCENDING))
    for index, status in enumerate(statuses):
        statusCode = status["statusCode"]
        if statusCode == "4":
            if statuses[index - 1]["statusCode"] == "47":
                print(ccn)

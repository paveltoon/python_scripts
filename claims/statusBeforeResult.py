from rldd.client import Client
from rldd import config
import pymongo

db = Client(config.PROD).connect()
claims = db["claims"].find({"service.srguServicePassportId": "5000000000166988901",
                            "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")},
                            "resultStatus": {'$exists': True}})
result3 = 0
result4 = 0
iteration = 0
for claim in claims:
    iteration += 1
    print(iteration)
    claim_id = claim["_id"]
    statuses = list(db["claims_status"].find({"claimId": str(claim_id)}).sort("statusDate", pymongo.ASCENDING))
    statusCode_list = []
    for index, status in enumerate(statuses):
        statusCode = status["statusCode"]
        if statusCode == "47":
            if statuses[index + 1]["statusCode"] == "4":
                result4 += 1
        if statusCode == "84":
            if statuses[index + 1]["statusCode"] == "3":
                result3 += 1
print(result3, result4)

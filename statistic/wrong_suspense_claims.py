from pymongo import ASCENDING
from rldd.client import Client
from rldd.config import PROD

result_file = open("wrong_claims.csv", "w+", newline="")

db = Client(PROD).connect()
claims = db["claims"].find({
    "activationDate": {"$gte": Client.ISODate("2021-01-01T00:00:00.000+0000")},
    "suspenseReason": {"$exists": True}
})
iteration = 0
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    statuses = list(db["claims_status"].find({
        "claimId": str(claimId),
        "statusCode": {
            "$in": [
                "70", "71"
            ]
        }
    }).sort("statusDate", ASCENDING))
    if statuses[0]["statusCode"] == "71":
        result_file.write(f"{ccn}\n")
        print(ccn, iteration)
result_file.close()

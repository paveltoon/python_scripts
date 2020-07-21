from bson import ObjectId

from rldd import rldd2
from user import rldd_user
import pymongo

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find({"activationDate": {'$gte': rldd2.ISODate("2019-12-31T21:00:00.000+0000")},
                            "service.srguServicePassportId": {'$ne': "5000000010000000897"},
                            "statuses.statusCode": "7"})
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    statuses = db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.ASCENDING)
    prevStatus = None
    for index, status in enumerate(statuses):

        statusCode = status["statusCode"]
        if prevStatus is None:
            prevStatus = statusCode
        if statusCode == "24" and prevStatus == "7":
            print(ccn)
            prevStatus = None
            continue
        prevStatus = statusCode

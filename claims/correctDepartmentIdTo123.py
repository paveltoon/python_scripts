from rldd.client import Client
from rldd.config import PROD

db = Client(PROD).connect()
claims = db["claims"].find({"service.srguServicePassportId": "5000000000215773980"})
result_file = open("correctedClaims.csv", "w+")
result_file.write(f"claimId;customClaimNumber\n")
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    service = claim["service"]
    if "srguDepartmentId" in service:
        if service["srguDepartmentId"].strip() == "":
            db["claims"].update_one({"_id": claimId}, {"$set": {"service.srguDepartmentId": "123"}})
            result_file.write(f"{claimId};{ccn}\n")
    else:
        db["claims"].update_one({"_id": claimId}, {"$set": {"service.srguDepartmentId": "123"}})
        result_file.write(f"{claimId};{ccn}\n")
result_file.close()
from bson import InvalidBSON

from rldd.client import Client
from rldd.config import PROD, DEV

db = Client(DEV).connect()
query = {"activationDate": {"$gte": Client.ISODate("2020-09-01T00:00:00.000+0000")}, "docSendDate": {"$exists": True}}
pjct = {"_id": 1, "deadlineDate": 1, "docSendDate": 1, "customClaimNumber": 1, "daysToDeadline": 1}

iteration = 0
total_count = db["claims"].count_documents(query)
while True:
    try:
        claims = db["claims"].find(query, pjct).skip(iteration)
        for claim in claims:
            iteration += 1
            claimId = claim["_id"]
            daysToDeadline = (claim["deadlineDate"] - claim["docSendDate"]).days + 1
            db["claims"].update_one({"_id": claimId}, {"$set": {
                "daysToDeadline": int(daysToDeadline)
            }})
            print(f"{iteration} / {total_count}", claim["_id"], daysToDeadline)
        break
    except InvalidBSON:
        iteration += 1
        continue

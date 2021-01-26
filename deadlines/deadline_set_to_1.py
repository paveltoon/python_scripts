from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
projection = {"_id": 1, "customClaimNumber": 1, "deadlineDate": 1, "docSendDate": 1}


def setDeadlineToOneDay(query):
    claims = db["claims"].find(query, projection)
    for claim in claims:
        ccn = claim["customClaimNumber"]
        claimId = claim["_id"]
        deadlineDate = claim["deadlineDate"]
        if "docSendDate" in claim:
            upd = db["claims"].update_one({"_id": claimId},
                                          {"$set": {"docSendDate": deadlineDate, "daysToDeadline": 1}})
            print(f"Claim: {ccn}, progress: {upd.modified_count} / {upd.matched_count}")

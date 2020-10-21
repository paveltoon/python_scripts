from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iteration = 0
jection = {"_id": 1, "currStatus": 1}
claims = db["claims"].find(
    {"service.srguServiceId":
        {'$in': [
            "5000000000184562222",
            "5000000000184561111"
        ]},
        "resultStatus": "3"}, jection)
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    updStatus = db["claims_status"].update_many({
        "claimId": str(claimId),
        "statusCode": "3"}, {
        "$set": {"additionalInfo": "DO_NOT_SEND_TO_LK"}
    })
    status = db["claims_status"].find_one({
        "claimId": str(claimId),
        "statusCode": "3"})
    del status["_class"]
    updClaim = db["claims"].update_one({"_id": claimId}, {"$set": {"currStatus": status}})
    print(f"{iteration}. Claim {claimId}. Status correct: {updStatus.modified_count} / {updStatus.matched_count}, Claim correct: {updClaim.modified_count} / {updClaim.matched_count}")

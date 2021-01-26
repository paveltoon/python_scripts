from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iteration = 0
claims = db["claims"].find({"resultStatus": "3", "currStatus.statusCode": "2"})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    status = db["claims_status"].update_many({"claimId": str(claimId), "statusCode": "3"},
                                             {"$set": {"additionalInfo": "DO_NOT_SEND_TO_LK"}})
    claim_statuses = claim["statuses"]
    for index, cs in enumerate(claim_statuses):
        if cs["statusCode"] == "3":
            path = f'statuses.{index}.additionalInfo'
            upd = db["claims"].update_one({"_id": claimId}, {"$set": {path: "DO_NOT_SEND_TO_LK"}})
            print(iteration, str(claimId), str(upd.modified_count) + ' / ' + str(upd.matched_count))

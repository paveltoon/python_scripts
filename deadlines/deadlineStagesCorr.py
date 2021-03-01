from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iteration = 0
claims = db["claims"].find(
    {"service.srguServiceId": {"$in": ["5000000010000181775", "5000000010000182114"]}, "consultation": False,
     "deadlineStages.stageType": "REGULATION_TIME", "deadlineStages.deadlineInWorkDays": False})
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    deadlineStages = claim["deadlineStages"]
    iteration += 1
    for index, stage in enumerate(deadlineStages):
        try:
            if stage["stageType"] == "REGULATION_TIME" and stage["deadlineInWorkDays"] == False:
                upd = db["claims"].update_one({"_id": claimId}, {
                    "$set": {
                        f"deadlineStages.{index}.deadlineInWorkDays": True
                    }
                })
                print(ccn)
        except KeyError as k:
            continue

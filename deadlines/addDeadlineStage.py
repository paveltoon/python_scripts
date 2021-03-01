from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claimsFile = open("claimIds.txt")
claimsList = claimsFile.read().split("\n")
resultFile = open("resultStages.csv", "w+", newline="")
resultFile.write("customClaimNumber\n")
for claimId in claimsList:
    claim = db["claims"].find_one({"_id": Client.getId(claimId)})
    if claim:
        if "resultStatus" in claim:
            continue
        upd = db["claims"].update_one({"_id": claim["_id"]},
                                      {"$push": {"deadlineStages": {
                                          "stageType": "DEADLINE_TRANSFER",
                                          "stageName": "Перенос регламентного срока",
                                          "deadline": 4,
                                          "deadlineInWorkDays": True
                                      }}})
        print(f"Claim {claim['customClaimNumber']} has been corrected: {upd.modified_count} / {upd.matched_count}")
        resultFile.write(f"{claim['customClaimNumber']};{upd.modified_count}\n")
resultFile.close()

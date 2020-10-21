from rldd import config
from rldd.client import Client

query = {"statusDate": {'$gte': Client.ISODate("2020-10-15T21:00:00.000+0000"),
                        '$lte': Client.ISODate("2020-10-20T21:00:00.000+0000")},
         "createDate": {'$gte': Client.ISODate("2020-09-22T21:00:00.000+0000"),
                        '$lte': Client.ISODate("2020-09-23T21:00:00.000+0000")}}
iteration = 0
count = 0
db = Client(config.PROD).connect()
claims = db["claims_status_mku"].find(query, {"claimId": 1})
for data in claims:
    iteration += 1
    isFound = False
    claimId = data["claimId"]
    claim = db["claims"].find_one({"_id": claimId})

    if claim is None:
        continue

    ccn = claim["customClaimNumber"]
    if "deadlineStages" in claim:
        for index, stage in enumerate(claim["deadlineStages"]):
            if "stageName" in stage:
                if stage["stageName"] == "Корректировка срока":
                    isFound = True

    if isFound:
        count += 1
        #upd = db["claims"].update_one({"_id": claimId}, {"$pull": {"deadlineStages": {"stageName": "Корректировка срока"}}})
        print(iteration, count, ccn)

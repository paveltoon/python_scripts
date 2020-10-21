from rldd.client import Client
from rldd import config

count = 0
query = {
    "deadlineDate": Client.ISODate("2020-10-01T21:00:00.000+0000"),
    "oktmo": {"$ne": "99999999"}
}
result_file = open('result_claims.csv', 'w+')
projection = {
    "_id": 1,
    "deadlineStages": 1,
    "customClaimNumber": 1
}
iteration = 0
db = Client(config.PROD).connect()
claims = db["claims"].find(query, projection)
for claim in claims:
    iteration += 1
    print(iteration)
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    deadlineStages = claim["deadlineStages"]
    for stage in deadlineStages:
        if stage["deadline"] < 0:
            count += 1
            print(count, ccn)
            result_file.write(f"{ccn}\n")
            # db["claims"].update_one({"_id": claimId}, {"$pull": {"deadlineStages": {"deadline": {"$lt": 0}}}})
            # db["claims"].update_one({"_id": claimId}, {"$pull": {"deadlineStages": {"stageName": "Корректировка срока"}}})
result_file.close()

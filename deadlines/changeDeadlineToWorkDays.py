from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
projection = {"_id": 1, "deadlineDate": 1, "docSendDate": 1, "customClaimNumber": 1}
result_file = open('claims_correct2.csv', 'w+')
result_file.write("Номер заявления;Предыдущая дата;Дата сейчас\n")
claims = db["claims"].find({
    "activationDate": {
        "$gte": Client.ISODate("2020-10-01T21:00:00.000+0000"),
        "$lte": Client.ISODate("2020-11-26T21:00:00.000+0000")
    },
    "resultStatus": {"$exists": True},
    "service.srguServicePassportId": "5000000000167433775"},
    projection)
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    deadlineDate = claim["deadlineDate"]
    if claim["docSendDate"] > claim["deadlineDate"]:
        upd = db["claims"].update_one({"_id": claimId}, {"$set": {"docSendDate": deadlineDate, "daysToDeadline": 1}})
        print(f"Claim: {ccn}, progress: {upd.modified_count} / {upd.matched_count}")
        result_file.write(f"{ccn};{claim['docSendDate']};{claim['deadlineDate']}\n")
result_file.close()

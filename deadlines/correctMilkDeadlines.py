from rldd.client import Client
from rldd import config
import csv
db = Client(config.PROD).connect()
with open('../deadMilk.csv') as csvfile:
    table = csv.reader(csvfile, delimiter=';')
    for row in table:
        ccn = row[3]
        claim = db["claims"].find_one({"customClaimNumber": ccn})
        if claim:
            claimId = claim["_id"]
            deadlineDate = claim["deadlineDate"]
            if "docSendDate" in claim:
                upd = db["claims"].update_one({"_id": claimId}, {"$set": {"docSendDate": deadlineDate, "daysToDeadline": 1}})
                print(f"Claim: {ccn}, progress: {upd.modified_count} / {upd.matched_count}")

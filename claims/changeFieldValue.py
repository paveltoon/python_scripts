import csv

from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
in_file = open('3174.csv', "r+")
claims = csv.reader(in_file, delimiter=';', dialect='excel')
for row in claims:
    ccn = row[0]
    oldNum = row[1]
    newNum = row[2]
    claim = db["claims"].find_one({"customClaimNumber": ccn})
    if claim:
        claimId = claim["_id"]
        try:
            fields = claim["fields"]["sequenceValue"]
        except KeyError:
            continue
        for index, field in enumerate(fields):
            try:
                if field["stringId"] == "namehospital":
                    upd = db["claims"].update_one(
                        {
                            "_id": claimId
                        },
                        {
                            "$set": {
                                f"fields.sequenceValue.{index}.value": newNum
                            }
                        }
                    )
                    print(f"{ccn} {upd.modified_count} / {upd.matched_count}")
            except KeyError:
                continue

from rldd.client import Client
from rldd import config
import csv

db = Client(config.PROD).connect()

with open("claimIds.csv", newline="") as csvfile:
    claims = csv.reader(csvfile, delimiter=";")
    for claim in claims:
        claimId = Client.getId(claim[0])

        cl = db["claims"].find_one({"_id": claimId})
        if cl:
            ccn = cl["customClaimNumber"]
            upd1 = db["claims_status"].delete_many({"claimId": str(claimId), "statusCode": "3"})
            upd2 = db["claims"].update_one({"_id": claimId}, {"$pull": {"statuses": {"statusCode": "3"}}})
            print(f"Claim {ccn}. claims_status deleted: {upd1.deleted_count}, statuses deleted: {upd2.modified_count}")

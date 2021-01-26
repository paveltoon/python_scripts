from rldd.client import Client
from rldd import config
import pymongo

db = Client(config.PROD).connect()
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-7082339825-40501650",
            "P001-4529289203-40599755",
            "P001-4529289203-40599321"
        ]
    }
})
for claim in claims:
    claimId = claim["_id"]
    status = db["claims_status"].delete_many({"claimId": str(claimId), "statusCode": "6", "senderCode": "RGIS05001"})
    status_in_claim_upd = db["claims"].update_one({"_id": claimId}, {
        "$pull": {"statuses": {"statusCode": "6", "senderCode": "RGIS05001"}}})

    statuses = list(db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.DESCENDING))
    last_status = statuses[0]
    del last_status["_class"]
    db["claims"].update_one({"_id": claimId}, {"$set": {"currStatus": last_status}})
    print(f"Claim {claim}. Removed: {status.deleted_count}. Updated in claim: {status_in_claim_upd.modified_count}")

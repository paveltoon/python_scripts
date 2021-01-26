from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()

statuses_to_remove = [
    "70",
    "71"
]

claims = db["claims"].find({"customClaimNumber": {"$in": [
    "P001-1054973946-41339758",
    "P001-1054973946-41339458",
    "P001-5137352317-40791164",
    "P001-9178059422-40814858",
    "P001-6687527427-40815941",
    "P001-9178059422-40814645"
]}})
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    upd1 = db["claims_status"].delete_many({"claimId": str(claimId), "statusCode": {"$in": statuses_to_remove}})
    upd2 = db["claims"].update_one({"_id": claimId}, {"$pull": {"statuses": {"statusCode": {"$in": statuses_to_remove}}}})
    print(f"Claim {ccn}. claims_status deleted: {upd1.deleted_count}, statuses deleted: {upd2.modified_count}")

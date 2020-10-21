from rldd.client import Client
from rldd import config
import pymongo
from datetime import datetime, timedelta

db = Client(config.DEV).connect()
claims = db["claims"].find().sort("activationDate", pymongo.DESCENDING).limit(100)
for claim in claims:
    deadlineDate = claim["deadlineDate"]
    result_dict = {
        "createDate": datetime.now() - timedelta(hours=3),
        "previousDeadlineDate": deadlineDate - timedelta(days=2),
        "nextDeadlineDate": deadlineDate,
        "claimId": str(claim["_id"])
    }
    db["claim_deadline_changes"].insert_one(result_dict)

import datetime

from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()

new_date = "2021-01-13"

projection = {
    "_id": 1,
    "activationDate": 1,
    "customClaimNumber": 1,
    "deadlineStages": 1,
    "deadlineDate": 1,
    "deadline": 1,
    "deadlineInWorkDays": 1
}
claims = db["claims"].find({"customClaimNumber": {"$in": [
    "P001-5137352317-40791164",
    "P001-9178059422-40814858",
    "P001-6687527427-40815941",
    "P001-9178059422-40814645"
]}})


def form_date(date: str):
    _unform_date = date.split('-')
    return datetime.datetime(int(_unform_date[0]), int(_unform_date[1]), int(_unform_date[2])) - datetime.timedelta(
        hours=3)


for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    activationDate = claim["activationDate"]
    deadlineDate = claim["deadlineDate"]
    count_of_days = (form_date(new_date) - deadlineDate).days if (form_date(
        new_date) - datetime.datetime.now()).days > 0 else 0
    if "deadlineStages" in claim:
        db["claims"].update_one({"_id": claimId}, {"$push": {"deadlineStages": {
            "deadline": count_of_days,
            "deadlineInWorkDays": False
        }}})

    print(deadlineDate + datetime.timedelta(days=count_of_days))

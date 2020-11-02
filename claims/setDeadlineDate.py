from bson import InvalidBSON

from rldd.client import Client
from rldd import config
from datetime import datetime, timedelta
import requests
from time import sleep

db = Client(config.PROD).connect()
newDate = datetime(2020, 10, 2) - timedelta(hours=3)
insert_count = 0
processed = 0
ind = 0
query = {
    "deadlineDate": {"$gte": Client.ISODate("2020-03-11T21:00:00.000+0000"),
                     "$lte": Client.ISODate("2020-10-01T20:00:00.000+0000")}
}

projection = {
    "_id": 1,
    "customClaimNumber": 1,
    "deadlineDate": 1,
    "deadlineStages": 1,
    "deadline": 1,
    "deadlineInWorkDays": 1,
    "activationDate": 1,
    "resultStatus": 1,
    "docSendDate": 1
}


def send_to_claim_deadline_changes(_claim_id, _previous_deadline_date, _next_deadline_date):
    __document = {
        "createDate": datetime.now() - timedelta(hours=3),
        "previousDeadlineDate": _previous_deadline_date,
        "nextDeadlineDate": _next_deadline_date,
        "claimId": _claim_id
    }

    _upd = db["claim_deadline_changes"].insert_one(__document)


def check_deadline_changes_queue():
    res = requests.get("http://10.10.80.54:8080/api/troubleshooting/claim-deadline-changes/notify")
    return res


while True:
    try:
        claims = db["claims"].find(query, projection, no_cursor_timeout=True).skip(processed)
        for claim in claims:
            claimId = claim["_id"]
            origDeadlineDate = claim["deadlineDate"]
            ccn = claim["customClaimNumber"]
            upd = db["claims"].update_one({"_id": claimId}, {"$set": {"deadlineDate": newDate}})
            if origDeadlineDate != newDate:
                send_to_claim_deadline_changes(str(claimId), origDeadlineDate, newDate)
            ind += 1
            print(ind, ccn, upd.modified_count, "/", upd.matched_count)
        check_deadline_changes_queue()
        break
    except InvalidBSON as e:
        print(e)
        processed += 1
    except:
        processed += 1
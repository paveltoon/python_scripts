from rldd.client import Client
from rldd import config

db = Client(config.DEV).connect()
upd = db["claims"].update_many({
    "deadlineDate": Client.ISODate("2020-10-01T21:00:00.000+0000"),
    "daysToDeadline": {'$gt': 1},
    "resultStatus": {"$exists": False}
},
    {
        "$pull": {"deadlineStages": {"stageName": "Корректировка срока"}}
    })
print(f"{upd.modified_count} / {upd.matched_count}")

from rldd.client import Client
from rldd import config
db = Client(config.PROD).connect()
query = {
    "activationDate": {"$gte": Client.ISODate("2020-03-11T21:00:00.000+0000")},
    "deadlineDate": {"$gte": Client.ISODate("2020-03-11T21:00:00.000+0000"),
                     "$lte": Client.ISODate("2020-10-02T20:00:00.000+0000")}
}
upd = db["claims"].update_many(query, {"$pull": {"deadlineStages": {"stageName": "Корректировка срока"}}})
print(upd.modified_count, "/", upd.matched_count)
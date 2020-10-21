from rldd.client import Client
from rldd import config

db = Client(config.DEV).connect()
upd = db["departments"].update_many({"department": {'$exists': True}}, {"$unset": {"department": ""}})
print(upd.modified_count, upd.matched_count)

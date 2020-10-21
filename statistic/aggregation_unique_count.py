from rldd.client import Client
from rldd import config
from bson.tz_util import FixedOffset
from datetime import datetime
from pymongo import MongoClient

database = Client(config.PROD).connect()
collection = database["claims"]

pipeline = [
    {"$match": {
        "service.srguServicePassportId": "5000000010000015448",
        "activationDate": {
            "$gte": Client.ISODate("2020-05-05T21:00:00.000+0000")
        }
    }},
    {
        "$count": "Total"
    }
]

pipeline2 = [
    {"$match": {
        "service.srguServicePassportId": "5000000010000015448",
        "activationDate": {
            "$gte": Client.ISODate("2020-05-05T21:00:00.000+0000")
        }
    }},
    {"$group": {
        "_id": "$persons",
        "count": {
            "$sum": 1
        }
    }},
    {
        "$count": "Unique"
    }
]

cursor = collection.aggregate(pipeline)
cursor2 = collection.aggregate(pipeline2)
result = {}
for doc in cursor:
    result["Total"] = doc["Total"]

for doc in cursor2:
    result["Unique"] = doc["Unique"]

print(result)
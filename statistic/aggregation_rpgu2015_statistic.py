from bson import Regex

from rldd.client import Client
from rldd import config

database = Client(config.PROD).connect()
# Год, по которому вести поиск в базе
year = 2018

collection = database[f"claims_{year}"]
result_file = open(f'IPGU01001_{year}.csv', "w+")

pipeline = [
    {
        u"$match": {
            u"service": {
                u"$exists": True
            },
            u"service.srguServicePassportId": {
                u"$not": Regex(u".*_444$", "i")
            },
            u"senderCode": u"IPGU01001"
        }
    },
    # {
    #     u"$limit": 100.0
    # },
    {
        u"$group": {
            u"_id": u"$service.srguServicePassportId",
            u"count": {
                u"$sum": 1.0
            }
        }
    }
]

cursor = collection.aggregate(
    pipeline,
    allowDiskUse=False
)
try:
    for doc in cursor:
        result_file.write(f'{doc["_id"]};{int(doc["count"])}\n')
finally:
    pass

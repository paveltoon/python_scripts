import datetime

from rldd.client import Client
from rldd.config import PROD

db = Client(PROD).connect()
year = 2021
calendar = db["calendars"].find_one({"year": year, "oktmo": ""})
daysOff = []
for day in calendar["daysOff"]:
    daysOff.append(datetime.datetime(year, 1, 1) + datetime.timedelta(day - 1) - datetime.timedelta(hours=3))
count = db["claims"].count_documents({
    "deadlineDate": {
        "$in": daysOff
    },
    "activationDate": {"$gte": Client.ISODate("2020-12-31T21:00:00.000+0000")}
})
print(count)

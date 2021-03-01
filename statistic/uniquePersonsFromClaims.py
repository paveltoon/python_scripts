from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({"senderCode": "IPGU01001",
                            "activationDate": {"$gte": Client.ISODate("2020-12-31T21:00:00.000+0000"),
                                               "$lte": Client.ISODate("2021-01-30T21:00:00.000+0000")}})
result_file = open("unique_persons.csv", 'w+')
iteration = 0
for claim in claims:
    iteration += 1
    try:
        for person in claim["persons"]:
            result_file.write(f"{person}\n")
            print(iteration)
    except KeyError as k:
        continue

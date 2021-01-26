from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iteration = 0
query = {"activationDate": {"$gte": Client.ISODate("2019-12-31T21:00:00.000+0000"),
                            "$lte": Client.ISODate("2020-12-03T21:00:00.000+0000")}}
projection = {
    "_id": 1,
    "customClaimNumber": 1,
    "service.srguServiceId": 1,
    "service.srguServiceName": 1,
    "service.name": 1,
    "service.srguDepartmentId": 1,
    "service.srguDepartmentName": 1,
    "service.srguServicePassportId": 1,
    "service.srguServicePassportName": 1,
}
total_count = 11460885
claims = db["claims"].find(query, projection).limit(10000)
for claim in claims:
    iteration += 1
    print(f"{iteration} / {total_count}")
    ccn = claim["customClaimNumber"]
    if "srguServicePassportName" not in claim["service"]:
        print(ccn)

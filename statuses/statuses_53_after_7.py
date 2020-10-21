import datetime

from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({"service.srguServiceId": "5000000000191297688",
                            "activationDate": {'$gte': Client.ISODate("2020-01-01T10:50:34.251+0000")}})

# claims = db["claims"].find({"customClaimNumber": "P001-6030412169-39476951"})

for claim in claims:
    ccn = claim["customClaimNumber"]
    if "statuses" in claim:
        for index, status in enumerate(claim["statuses"]):
            statDate = None
            if status["statusCode"] == "53":
                statDate = status["statusDate"]
                if claim["statuses"][index - 1]["statusCode"] == "7":
                    if statDate - claim["statuses"][index - 1]["statusDate"] > datetime.timedelta(hours=1):
                        print(ccn)

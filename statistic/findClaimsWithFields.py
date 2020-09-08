from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
res_file = open('res.csv', 'w+')
claims = db["claims"].find({"service.srguServicePassportId": "5000000000188307694",
                            "activationDate": {'$gte': Client.ISODate("2020-08-01T00:00:00.000+0000")}})
for claim in claims:
    if "fields" not in claim:
        continue
    ccn = claim["customClaimNumber"]
    isCorrect = True
    fields = claim["fields"]["sequenceValue"]
    for seq in fields:
        if "stringId" in seq:
            if seq["stringId"] == "proshuvkldtp" \
                    or seq["stringId"] == "proshuvklPZZ" \
                    or seq["stringId"] == "proshuvklPPT":
                isCorrect = False
    if isCorrect:
        res_file.write(f"{ccn}\n")

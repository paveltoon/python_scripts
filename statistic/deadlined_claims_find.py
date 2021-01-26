from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
result_file = open('result.csv', 'w+')
result_file.write("customClaimNumber;deadlineDate;docSendDate\n")
claims = db["claims"].find({"service.srguServicePassportId": "5000000000196795211", "resultStatus": {"$exists": True}})
for claim in claims:
    claimId = claim["_id"]
    status70 = db["claims_status"].find_one({"claimId": str(claimId), "statusCode": "70"})
    if status70:
        days = (claim["deadlineDate"] - claim["docSendDate"]).days
        if days < 0:
            print(claim['customClaimNumber'])
            result_file.write(f"{claim['customClaimNumber']};{claim['deadlineDate']};{claim['docSendDate']}\n")
result_file.close()

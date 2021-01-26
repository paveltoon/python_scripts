from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({
    "service.srguServicePassportId": "5000000000186738813",
    "resultStatus": {"$exists": True},
    "docSendDate": {"$gte": Client.ISODate("2020-08-31T21:00:00.000+0000")}
})
result_file = open("claims_without_result_docs.csv", "w+")
result_file.write("customClaimNumber;docSendDate;resultStatus;service.name\n")
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    docs = list(db["docs"].find({"ownerId": str(claimId), "title": {"$regex": "^Результат.*"}}))
    if len(docs) == 0:
        print(ccn)
        result_file.write(f"{ccn};{claim['docSendDate'].isoformat()};{claim['resultStatus']};{claim['service']['name']}\n")
result_file.close()

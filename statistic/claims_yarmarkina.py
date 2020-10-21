from rldd.client import Client
from rldd import config

result_file = open('claims_result.csv', 'w+')
result_file.write("customClaimNumber;statusDate\n")

claims_list = open('claims.txt', 'r+').read().split('\n')
iteration = 0

jop = {"_id": 1, "activationDate": 1, "customClaimNumber": 1, "resultStatus": 1, "docSendDate": 1}
db = Client(config.PROD).connect()
claims = db["claims"].find({"customClaimNumber": {"$in": claims_list},
                            "resultStatus": {"$exists": True},
                            "activationDate": {"$gte": Client.ISODate("2019-11-30T21:00:00.000+0000"),
                                               "$lte": Client.ISODate("2020-01-08T21:00:00.000+0000")},
                            "docSendDate": {"$lte": Client.ISODate("2020-01-27T21:00:00.000+0000")}}, jop,
                           no_cursor_timeout=True)
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]

    statuses = list(db["claims_status"].find({"claimId": str(claimId), "statusCode": {"$in": ["34", "53"]}}))
    if len(statuses) == 2:
        statusDate = None
        for status in statuses:
            if status["statusCode"] == "53":
                statusDate = status["statusDate"].isoformat()
        result_file.write(f"{ccn};{statusDate}\n")
        print(iteration, ccn)

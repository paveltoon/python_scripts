import datetime

from rldd.client import Client
from rldd import config

result_file = open('result.csv', 'w+')
db = Client(config.PROD).connect()
claims = db["claims"].find(
    {
        "deadlineDate": {'$gte': Client.ISODate("2020-10-03T21:00:00.000+0000")},
        "suspenseReason": {'$exists': True},
        "senderCode": {'$ne': "RRTR01001"}
    }
)
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    deadlineDate = claim["deadlineDate"]
    endDate = claim["docSendDate"] if "docSendDate" in claim else datetime.datetime.now()
    if (deadlineDate - endDate).days < 0:
        print(ccn)
        result_file.write(f"{ccn}\n")
result_file.close()

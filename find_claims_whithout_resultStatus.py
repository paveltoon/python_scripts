from bson import InvalidBSON

from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iteration = 0

projection = {
    "_id": 1,
    "customClaimNumber": 1,
    "resultStatus": 1,
    "service": 1,
    "currStatus": 1,
    "senderCode": 1
}

statuses_projection = {
    "statusCode": 1,
}

result_file = open('claims_without_result.csv', 'w+')
result_file.write('customClaimNumber;\n')
query = {"activationDate": {'$gte': Client.ISODate("2020-12-15T21:00:00.000+0000")},
         "resultStatus": {'$exists': False}}

query1 = {"customClaimNumber": "P001-0259864459-40561582"}
while True:
    try:
        claims = db["claims"].find(query, projection, no_cursor_timeout=True).skip(iteration)
        for claim in claims:
            iteration += 1
            print(iteration)
            claim_id = claim["_id"]
            ccn = claim["customClaimNumber"]
            status = db["claims_status"].find_one({"claimId": str(claim_id), "statusCode": {"$in": ["3", "4"]}}, statuses_projection)
            if status:
                claim = db["claims"].find_one({"customClaimNumber": ccn}, projection)
                if "resultStatus" not in claim:
                    result_file.write(f"{ccn};{claim['service']['name']};{claim['currStatus']['statusCode']};{claim['senderCode']}\n")
        break
    except InvalidBSON:
        iteration += 1

result_file.close()

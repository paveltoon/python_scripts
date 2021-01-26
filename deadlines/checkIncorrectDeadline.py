from bson import InvalidBSON

from rldd.client import Client
from rldd import config
from datetime import timedelta

db = Client(config.PROD).connect()

result_file = open("wrongDeadline.csv", 'w+', newline="")
result_file.write("customClaimNumber;deadlineDate;activationDate;name;srguServiceId;isSuspense\n")
query = {"activationDate": {"$gte": Client.ISODate("2019-12-31T21:00:00.000+0000")}}
pr = {"_id": 1, "customClaimNumber": 1, "deadlineDate": 1, "activationDate": 1, "service": 1, "suspenseReason": 1}
total_count = db["claims"].count_documents(query)
current_step = 0
while True:
    try:
        claims = db["claims"].find(query, pr).skip(current_step)
        for claim in claims:
            current_step += 1
            print(f"{current_step} / {total_count}")
            try:
                if claim["deadlineDate"] < claim["activationDate"] - timedelta(minutes=1):
                    susReason = True if 'suspenseReason' in claim else False
                    serviceName = claim['service']['name'].replace('\n', '').replace('\r', '').replace('\t', '')
                    print(claim['customClaimNumber'])
                    result_file.write(
                        f"{claim['customClaimNumber']};{claim['deadlineDate']};{claim['activationDate']};{serviceName};{claim['service']['srguServiceId']};{susReason}\n")
            except KeyError:
                continue
        break
    except InvalidBSON as e:
        current_step += 1
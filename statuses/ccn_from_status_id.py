import csv
from rldd.client import Client
from rldd import config
res_file = open('newData.csv', 'w+')
res_file.write("statusId;claimId;customClaimNumber\n")
iteration = 0
with open('data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        iteration += 1
        _id = row[0]
        db = Client(config.PROD).connect()
        status = db["claims_status"].find_one({"_id": Client.getId(_id)})
        if status:
            claim = db["claims"].find_one({"_id": Client.getId(status["claimId"])})
            claimId = claim["_id"]
            ccn = claim["customClaimNumber"]
            print(f"{iteration} {_id} {ccn}")
            res_file.write(f"{_id};{claimId};{ccn}\n")
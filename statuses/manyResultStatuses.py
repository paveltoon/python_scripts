import pymongo
from bson import InvalidBSON

from rldd.client import Client
from rldd import config

corrected = 0
wrongs = open('wrongs.csv', 'w+')
wrongs.write("claimId;customClaimNumber;Error\n")
rights = open('rights.csv', 'w+')
rights.write("claimId;customClaimNumber;FirstStatusDate;DocSendDate;Deadline correct\n")
db = Client(config.PROD).connect()
iteration = 0
isDead = False
projection = {
    "_id": 1,
    "activationDate": 1,
    "customClaimNumber": 1,
    "deadlineDate": 1,
    "docSendDate": 1
}
while True:
    try:
        claims = db["claims"].find(
            {"docSendDate": {"$exists": True}, "senderCode": {"$ne": "RRTR01001"}, "resultStatus": {"$exists": True},
             "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")}},
            projection, no_cursor_timeout=True).skip(iteration)
        for claim in claims:
            try:
                claimId = claim["_id"]
                ccn = claim["customClaimNumber"]
                activationDate = claim["activationDate"]
                deadlineDate = claim["deadlineDate"]
                docSendDate = claim["docSendDate"]
                iteration += 1
                statuses = list(
                    db["claims_status"].find({"claimId": str(claimId), "statusCode": {"$in": ["3", "4"]}}).sort(
                        "statusDate",
                        pymongo.ASCENDING))
                if len(statuses) <= 1:
                    continue

                if statuses[0]["statusDate"] < activationDate:
                    wrongs.write(f"{claimId};{ccn};Wrong statusDate\n")
                    print(iteration, claimId, "wrongDate", corrected)
                    continue

                statusDate = statuses[0]["statusDate"].strftime("%d/%m/%Y")
                formattedDocSendDate = docSendDate.strftime("%d/%m/%Y")
                if statusDate != docSendDate.strftime("%d/%m/%Y"):
                    if (deadlineDate - docSendDate).days <= -1:
                        db["claims"].update_one({"_id": claimId}, {"$set": {"docSendDate": statuses[0]["statusDate"]}})
                        corrected += 1
                        print(iteration, ccn, statusDate, formattedDocSendDate, corrected)
                        if (deadlineDate - statuses[0]["statusDate"]).days > -1:
                            isDead = True
                        rights.write(f"{claimId};{ccn};{statusDate};{formattedDocSendDate};{isDead}\n")
            except KeyError:
                continue
            except:
                continue
        break
    except InvalidBSON as e:
        print(e)
        iteration += 1
rights.write(f"Total;{corrected}\n")
print(corrected)

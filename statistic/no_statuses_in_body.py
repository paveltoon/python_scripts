from rldd.client import Client
from rldd import config
import pymongo

result_file = open('statuses.csv', 'w+')
iteration = 0


def get_statuses(arr):
    obj = []
    for _s in arr:
        idPrefix = "_id" if "_id" in _s else "id"
        obj.append(str(_s[idPrefix]))
    return obj


db = Client(config.PROD).connect()
claims = db["claims"].find({"activationDate": {'$gte': Client.ISODate("2020-09-21T00:00:00.000+0300"),
                                               '$lte': Client.ISODate("2020-09-28T00:00:00.000+0300")},
                            "oktmo": {'$ne': "99999999"}}, {"statuses": 1, "_id": 1, "customClaimNumber": 1}, no_cursor_timeout=True)
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"] if "customClaimNumber" in claim else claimId
    if "statuses" not in claim:
        result_file.write(f"{claimId};{ccn};;статусы в теле заявки отсутствуют\n")
        continue

    body_statuses = get_statuses(claim["statuses"])

    statuses = list(
        db["claims_status"].find({"claimId": str(claimId)}, {"statusCode": 1, "statusDate": 1, "_id": 1}).sort(
            "statusDate", pymongo.ASCENDING))
    claims_statuses = get_statuses(statuses)
    result_list = list(set(claims_statuses) - set(body_statuses))
    if len(result_list) > 0:
        ids = ", ".join(result_list)
        codes = []
        for res in result_list:
            status = db["claims_status"].find_one({"_id": Client.getId(res)})
            codes.append(status["statusCode"])
        codes = ", ".join(codes)
        result_file.write(f"{claimId};{ccn};{ids};{codes}\n")
    print(iteration)

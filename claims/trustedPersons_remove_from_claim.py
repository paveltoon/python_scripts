from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find(
    {"activationDate": {'$gte': rldd2.ISODate("2020-09-01T00:00:00.841+0000"),
                        '$lte': rldd2.ISODate("2020-09-11T00:00:00.841+0000")},
     "resultStatus": {'$exists': False},
     "personsInfo.0.trustedPersons.0.trustedId": {'$exists': True}, "senderCode": "IPGU01001",
     "trustedPersons": {'$exists': False}})
result_file = open('trustedPersons.log', 'w+')
for claim in claims:
    _id = claim["_id"]
    try:
        ccn = claim['customClaimNumber']
        personsInfo = claim["personsInfo"]
        isTrusted = False
        if "trustedPersons" not in claim or not len(claim['trustedPersons']):
            for person in personsInfo:
                if "trustedPersons" in person:
                    del person["trustedPersons"]
                    isTrusted = True
        if isTrusted:
            upd = db["claims"].update_one({"_id": _id}, {"$set": {"personsInfo": personsInfo}})
            print(f'{ccn} {upd.modified_count} / {upd.matched_count}')
            result_file.write(f'{ccn} {upd.modified_count} / {upd.matched_count}\n')
    except Exception as err:
        print(f'{_id} ERROR: {err}')
result_file.close()

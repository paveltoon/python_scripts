from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find(
    {"personsInfo.trustedPersons.trustedId": {'$exists': True}, "personsInfo.type": {'$in': ["PHYSICAL", "IP"]},
     "trustedPersons.trustedPersonId": {'$exists': False}})
result_file = open('trustedPersons.log', 'w+')
for claim in claims:
    try:
        _id = claim["_id"]
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

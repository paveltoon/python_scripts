from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
remote = rldd2.REMOTE_connect()
projection = {"_id": 1, "service": 1, "creatorDeptId": 1}
claims = db['claims'].find({"activationDate": {'$gte': rldd2.ISODate("2019-12-31T21:00:00.000+0000")},
                            "service.srguServiceName": {'$exists': False}}, projection, no_cursor_timeout=True)
for claim in claims:
    if "service" not in claim:
        continue
    if "srguServiceId" not in claim["service"]:
        continue

    claimId = claim["_id"]

    if "name" in claim["service"]:
        upd1 = db['claims'].update_one({"_id": claimId}, {"$set": {"service.srguServiceName": claim["service"]["name"]}})
        print(f'Claim {claimId} has been updated. Progress: {upd1.modified_count} / {upd1.matched_count}')
        continue

    serviceId = claim["service"]["srguServiceId"]
    dbName = str

    if "creatorDeptId" in claim:
        if claim["creatorDeptId"].strip() != '':
            dbName = claim["creatorDeptId"]
        else:
            dbName = "mfc-etalon"
    else:
        dbName = "mfc-etalon"

    srgu = remote[dbName]["services"].find_one({"serviceIdSrgu": serviceId})

    if srgu is None:
        print(f'Claim {claimId} have no service at remote DB')
        continue

    serviceName = srgu['fullName']
    upd = db['claims'].update_one({"_id": claimId}, {"$set": {"service.srguServiceName": serviceName}})
    print(f'Claim {claimId} has been updated. Progress: {upd.modified_count} / {upd.matched_count}')

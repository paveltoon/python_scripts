from rldd import rldd2
from user import rldd_user
from datetime import datetime

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
local = rldd2.LOCAL_connect('local')
claims = db["claims"].find({
    "oktmo": "46000000",
    "$and": [{
        "service.srguServicePassportId": {
            "$ne": "5000000000196394746"
        }}, {
        "service.srguServicePassportId": {
            "$ne": "5000000000167433775"
        }}, {
        "service.srguServicePassportId": {
            "$ne": "5000000000160299214"
        }
    }],
    "provLevel": "ОМСУ",
    "claimCreate": {"$gte": rldd2.isodate("2019-08-05T01:03:09.046+0000")}
})
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    fields = claim["fields"]["sequenceValue"]
    isFounded = False

    for field in fields:
        if "stringId" in field and field["stringId"] == "municipality":
            oktmo = field["value"]
            localClaim = {
                "customClaimNumber": ccn,
                "oldOktmo": claim["oktmo"],
                "newOktmo": oktmo,
                "createDate": datetime.today()
            }
            local["claims"].insert_one(localClaim)
            upd = db["claims"].update_one({
                "_id": claimId
            }, {
                "$set": {
                    "oktmo": oktmo
                }
            })
            print(f'{ccn}, oktmo: {oktmo}. Updated progress: {upd.modified_count} / {upd.matched_count}')
            isFounded = True
            break
    if not isFounded:
        print(ccn)

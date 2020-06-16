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
    "claimCreate": {"$gte": rldd2.ISODate("2020-01-10T21:00:00.000+0000")}
})
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    isFounded = False
    try:
        fields = claim["fields"]["sequenceValue"]
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
                continue
        if not isFounded:
            print(ccn)
    except KeyError:
        print(f"{ccn} keyError")

from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({
    "service.srguServiceId": "5000000000195867143",
    # "service.srguServicePassportId": "5000000010000000897",
    "personsInfo.esiaAutorisation": True
})
for claim in claims:
    claimId = claim["_id"]
    ccn = claim['customClaimNumber']
    personsInfo = claim['personsInfo']
    for index, person in enumerate(personsInfo):
        updater = {}
        if 'esiaAutorisation' in person:
            if person['esiaAutorisation']:
                updater[f'personsInfo.{index}.esiaAutorisation'] = False
                upd = db['claims'].update_one({"_id": claimId}, {'$set': updater})
                print(f'Claim {ccn} has been updated. progress: {upd.modified_count} / {upd.matched_count}')

from rldd import rldd2
from user import rldd_user
import requests

query = {
    "service.srguServicePassportId": "5000000000198312020",
    "customClaimNumber": {'$regex': '^P001.*'},
    "oktmo": {'$in': ["55555555", "46000000"]}
}

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find(query)

for claim in claims:
    claim_id = claim['_id']
    ccn = claim['customClaimNumber']
    isOKTMOFinded = False
    oktmo = str
    if 'fields' in claim and 'sequenceValue' in claim['fields']:
        sequence = claim['fields']['sequenceValue']
        for field in sequence:
            if field['title'] == "Выберите МФЦ":
                dataSeq = field['sequenceValue']
                for ds in dataSeq:
                    if ds['title'] == "ОКТМО":
                        oktmo = ds['value']
                        isOKTMOFinded = True
    else:
        print(f"Claim {ccn} have no 'fields'.")
        continue

    if not isOKTMOFinded:
        print(f"Claim {ccn} have no OKTMO in fields")
        continue

    post_status = rldd2.postStatus(str(claim_id), 6, "Статус создан автоматически через РЛДД, для корректного закрытия заявки, в рамках тикета PGUSVC-3456")

    if 200 <= post_status.status_code <= 300:

        upd = db['claims'].update_one({
            "_id": claim_id
        }, {
            '$set': {
                "placeOfIssue": "MFC",
                "oktmo": oktmo
            }
        })
        print(f"Claim {ccn} has been updated. Progress: {upd.modified_count} / {upd.matched_count}.")
    else:
        print(f"Cant post status to claim {ccn}")

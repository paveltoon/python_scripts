from rldd.client import Client
from rldd import config

back_to_status = 39  # К какому статусу откатить

claims_list = [
    "P001-1787579005-35728043"
]

client = Client(config.PROD)
db = client.connect()
claims = db["claims"].find({"customClaimNumber": {"$in": claims_list}})

for claim in claims:
    claimId = claim["_id"]
    try:
        ccn = claim["customClaimNumber"]
        statuses = db["claims_status"].find({"claimId": str(claimId), "statusCode": {"$in": ["3", "4"]}})

        for status in statuses:
            statusId = status["_id"]
            docs = db["docs"].find({"ownerId": str(statusId)})

            for doc in docs:
                md5 = doc["fileMetadata"]["md5"]
                # Удаление доков привязанных к статусу с результатом
                delete_doc = db["docs"].delete_many({"ownerType": "CLAIM", "fileMetadata.md5": str(md5)})
                print(f"md5: {md5}, deleted: {delete_doc.deleted_count} docs.")
        # Удаление из заявки атрибутов resultStatus, docSendDate
        upd = db["claims"].update_one({"_id": claimId}, {"$unset": {"resultStatus": "", "docSendDate": ""}})
        # Пост статуса в заявку
        client.postStatus(claimId, back_to_status)
        print(f"Claim: {ccn}. Progress: {upd.modified_count} / {upd.matched_count}")

    except KeyError as k_e:
        print(claimId, k_e)
        continue
    except AttributeError as a_e:
        print(claimId, a_e)
        continue

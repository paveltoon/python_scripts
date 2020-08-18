from rldd import rldd2
from user import rldd_user
import pymongo

taskNum = "PGUSVC-3958"
comment = f"Статус проставлен автоматически через РЛДД в рамках тикета {taskNum}."
result_statuses_arr = ["3", "4", "81"]
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)

claims = db['claims'].find({"customClaimNumber": "P001-0264889448-37180548"})

for claim in claims:
    claimId = claim["_id"]

    isResult = False
    newStatus = None
    result_docs = []
    md5_list = []
    docs_to_delete = []
    # Find statuses
    statuses = list(db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.ASCENDING))
    for index, status in enumerate(statuses):
        if status["statusCode"] in result_statuses_arr:
            if not isResult:
                isResult = True
                newStatus = statuses[index - 1]["statusCode"]
            result_docs.append(str(status["_id"]))
    # Find docs
    if len(result_docs) != 0:
        status_docs = db["docs"].find({"ownerId": {'$in': result_docs}})
        for doc in status_docs:
            if "fileMetadata" in doc:
                if not doc["fileMetadata"]["md5"] in md5_list:
                    md5_list.append(doc["fileMetadata"]["md5"])
        claim_docs = db["docs"].find({"ownerId": str(claimId), "fileMetadata.md5": {'$in': md5_list}})
        for doc in claim_docs:
            docs_to_delete.append(doc["_id"])
    # Check & update
    if isResult and newStatus is not None:
        # rldd2.postStatus(claimId, newStatus, comment)
        # upd = db["claims"].update_one({claimId}, {"$unset": {"resultStatus": "", "docSendDate": ""}})
        if len(docs_to_delete) != 0:
            # rem = db["docs"].remove({"_id": {"$in": docs_to_delete}})
            pass

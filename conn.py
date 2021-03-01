import json

import bson

from rldd.client import Client
from rldd.config import PKPVD, DEV

db = Client(PKPVD, "pvdrs").connect()
phone_db = Client(DEV).connect()

result_file = open("result_jrnl.csv", "w+", newline="")

# docs = db["jrnl_gmp"].find({
#     "when": {
#         "$gte": Client.ISODate("2021-02-01T00:00:00.000+0000")
#     }
# })
#
# for doc in docs:
#     try:
#         body = doc["restJournalCall"]["responseBody"]
#         supplierBillId = json.loads(body)["quittances"][0]["supplierBillId"]
#         phone_db["xxx_jrnl_gmp"].insert_one({
#             "_id": bson.objectid.ObjectId(),
#             "docId": doc["_id"],
#             "substanceId": doc["substanceId"],
#             "requestNumber": doc["requestNumber"],
#             "supplierBillId": supplierBillId
#         })
#         print(supplierBillId)
#     except KeyError:
#         continue
#     except IndexError:
#         continue
#     except TypeError:
#         continue
#     except json.decoder.JSONDecodeError:
#         continue
#
# input("Нажмите enter, чтобы продолжить...")

claims = phone_db["xxx_jrnl_gmp"].find()
iteration = 0
for claim in claims:
    iteration += 1
    print(iteration)
    requestNumber = claim["requestNumber"]
    supplierBillId = claim["supplierBillId"]
    ids = list(phone_db["xxx_jrnl_gmp"].find({"supplierBillId": supplierBillId}))
    if len(ids) > 1:
        result_file.write(f"{claim['docId']};{claim['substanceId']};{requestNumber};{supplierBillId}\n")
        print(requestNumber)

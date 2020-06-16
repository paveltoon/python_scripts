import math

from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
req = {"claimCreate": {'$gte': rldd2.ISODate("2018-12-31T21:00:00.000+0000"),
                       '$lte': rldd2.ISODate("2019-12-31T21:00:00.000+0000")},
       "oktmo": {'$ne': "99999999"},
       "consultation": False
       }

# Variables

rpgu_all = 0
rpgu_result = 0
etc_all = 0
etc_result = 0

current_step = 0
total_count = db["claims"].find(req).count()

# Code
claims = db["claims"].find(req)
for claim in claims:
    current_step += 1
    progress = math.floor((current_step / total_count) * 100)
    claim_id = claim["_id"]
    try:
        if "senderCode" in claim:
            claim_sender_code = claim["senderCode"]
            docs = db["docs"].find({"ownerId": str(claim_id)})
            for doc in docs:
                if claim['senderCode'] == "IPGU01001":
                    rpgu_all += 1
                else:
                    etc_all += 1
                if "title" in doc:
                    if doc['title'].find("Результат") != -1 \
                            or doc['title'].find("Решение") != -1 \
                            or doc['title'].find("Отказ") != -1:
                        if claim['senderCode'] == "IPGU01001":
                            rpgu_result += 1
                        else:
                            etc_result += 1
        if current_step % 10000 == 0:
            print(f"{current_step} / {total_count}. {progress}%")
    except KeyError as k:
        print(claim_id, k)

print(rpgu_all, etc_all, rpgu_result, etc_result)

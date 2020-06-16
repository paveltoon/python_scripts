from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db['claims'].find({"service.srguServicePassportId": "5000000000189808193",
                            "activationDate": {'$gte': rldd2.ISODate("2020-05-08T21:00:00.000+0000")}})
for claim in claims:
    _id = claim['_id']
    ccn = claim['customClaimNumber']
    docs_count = db['docs'].count_documents({'ownerId': str(_id)})
    if docs_count == 0:
        print(f'{ccn}')

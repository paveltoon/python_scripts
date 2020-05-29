from rldd import rldd2
from user import rldd_user
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find({ "service.srguServicePassportId": "5000000010000047449" })
for claim in claims:
    _id = claim['_id']
    try:
        ccn = claim['customClaimNumber']
        statuses = db["claims_status"].find({'claimId': str(_id)})
        statuses_list = []
        for status in statuses:
            statuses_list.append(status["statusCode"])
    except Exception as err:
        print(f'{str(_id)}, {err}')
    if '41' in statuses_list and '58' in statuses_list and '24' not in statuses_list and '42' not in statuses_list:
        print(ccn)

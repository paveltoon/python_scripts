from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
statuses = db['claims_status'].find(
    {"statusDate": {'$gte': rldd2.ISODate("2018-12-31T21:00:00.000+0000")}, "statusCode": "43", "senderCode": "00000",
     "senderName": "ЕПГУ", "comment": {'$regex': '.*PIN-код.*'}})
result_file = open('statuses.csv', 'w+')
count = 0
result_file.write("customClaimNumber;Collection\n")
for status in statuses:
    count += 1
    claimId = rldd2.getId(status['claimId'])
    claim = db['claims'].find_one({"_id": claimId})
    if claim is not None:
        result_file.write(f"{claim['customClaimNumber']};claims\n")
    else:
        claim = db['claims_2018'].find_one({"_id": claimId})
        result_file.write(f"{claim['customClaimNumber']};claims_2018\n")
    print(count)
result_file.close()

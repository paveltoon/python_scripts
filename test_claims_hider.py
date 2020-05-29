from rldd import rldd2
from user import rldd_user
# CONNECTION
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
# FILE
read_file = open('C://MAP/map.txt').read()
result_file = open('./test_claims_hide.log', 'w+', encoding='utf-8')
ccn = read_file.split("\n")
# Program code
for claim in ccn:
    cursor = db["claims"].find_one({"customClaimNumber": claim})
    if cursor is not None:
        updateData = {
            "oktmo": "99999999"
        }
        if "deptId" in cursor:
            updateData["deptId"] = "mfc"
        if "creatorDeptId" in cursor:
            updateData["creatorDeptId"] = "mfc"
        if "service" in cursor and "srguServiceId" in cursor["service"]:
            serviceId = cursor["service"]["srguServiceId"]
            if serviceId.find("_444") == -1:
                updateData["service.srguServiceId"] = f'{serviceId}_444'
        upd = db["claims"].update_one(
            {"customClaimNumber": claim},
            {"$set": updateData}
        )
        result_print = f'Claim: {claim} progress: {upd.modified_count} / {upd.matched_count}'
        print(result_print)
        result_file.write(f'{result_print}\n')
    else:
        print(f'Claim: {claim} is not found.')
        result_file.write(f'Claim: {claim} is not found.\n')
result_file.close()

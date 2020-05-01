from rldd import rldd2
# CONNECTION
db = rldd2.LOCAL_connect("local")
# FILE
file = open('C://MAP/map.txt').read()
ccn = file.split("\n")
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
        print(f'Claim: {claim} progress: {upd.modified_count} / {upd.matched_count}')
    else:
        print(f'Claim: {claim} is not found.')

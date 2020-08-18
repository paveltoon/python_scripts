from rldd import rldd2
from user import rldd_user

db = rldd2.DPS_connect(rldd_user.login, rldd_user.pwd)
persons = db['persons'].find({"technicalProperties.type": "GOLD"})
for person in persons:
    personId = person["_id"]
    contacts = person["contacts"]
    found = False
    for contact in contacts:
        if "type" in contact:
            if contact["type"] == "PHN" or contact["type"] == "MBT":
                found = True
                break
    if not found:
        print(personId)

from rldd import rldd2
from user import rldd_user

itera = 0
result_file = open('result.csv', 'w+')
db = rldd2.DPS_connect(rldd_user.login, rldd_user.pwd)
persons = db['persons'].find({
    "technicalProperties.type": "GOLD"
}, {"surname": 1, "firstName": 1, "needToResearch": 1, "dateOfBirth": 1, "contacts": 1, "identityDocuments": 1})
for person in persons:

    itera += 1
    if itera % 1000 == 0:
        print(itera)
    if "needToResearch" in person:
        result = {
            "firstName": False,
            "surname": False,
            "dateOfBirth": False,
            "identityDocuments": False,
            "phone": False
        }

        personId = person["_id"]

        if "contacts" in person:
            contacts = person["contacts"]
            for contact in contacts:
                if "type" in contact:
                    if contact["type"] == "PHN" or contact["type"] == "MBT":
                        result["phone"] = True
                        break

        if "surname" in person:
            if person["surname"].strip() != '':
                result['surname'] = True

        if "firstName" in person:
            if person["firstName"].strip() != '':
                result['firstName'] = True

        if "dateOfBirth" in person:
            if person["dateOfBirth"].strip() != '':
                result['dateOfBirth'] = True

        if "identityDocuments" in person:
            result['identityDocuments'] = True

        if result['firstName'] and result['surname'] and result['dateOfBirth'] and result['identityDocuments'] and \
                result['phone']:
            upd = db['persons'].update_one({"_id": personId}, {"$unset": {"needToResearch": ""}})
            print(f'{personId};{upd.modified_count} / {upd.matched_count}')
            result_file.write(f'{personId};{upd.modified_count} / {upd.matched_count}\n')
result_file.close()
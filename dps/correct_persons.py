from rldd import rldd2
from user import rldd_user

result_file = open('result.csv', 'w+')
result_file.write(f"Person ID;Research status")
itera = 0
db = rldd2.DPS_connect(rldd_user.login, rldd_user.pwd)
projection = {
    "surname": 1,
    "firstName": 1,
    "needToResearch": 1,
    "middleName": 1,
    "gender": 1,
    "dateOfBirth": 1,
    "registrationAddressId": 1,
    "contacts": 1,
    "identityDocuments": 1,
    "technicalProperties": 1,
    "snils": 1
}

persons = db["persons"].find({
    "technicalProperties.type": "GOLD"
}, projection)

for person in persons:

    result = {
        "firstName": False,
        "surname": False,
        "dateOfBirth": False,
        "phone": False,
        "needToResearch": False
    }

    itera += 1
    if itera % 1000 == 0:
        print(itera)

    personId = person["_id"]

    if "needToResearch" in person:
        result['needToResearch'] = True

    if "surname" in person:
        if person["surname"].strip() != '':
            result['surname'] = True

    if "firstName" in person:
        if person["firstName"].strip() != '':
            result['firstName'] = True

    if "dateOfBirth" in person:
        if person["dateOfBirth"].strip() != '':
            result['dateOfBirth'] = True

    if "contacts" in person:
        contacts = person["contacts"]
        for contact in contacts:
            if "type" in contact:
                if contact["type"] == "PHN" or contact["type"] == "MBT":
                    result["phone"] = True

    if result["firstName"]\
            and result["surname"]\
            and result["dateOfBirth"]\
            and result["phone"]\
            and not result["needToResearch"]:
        continue

    if result["firstName"] \
            and result["surname"]\
            and result["dateOfBirth"]\
            and result["phone"]\
            and result["needToResearch"]:
        uns = db["persons"].update_one({"_id": personId}, {"$unset": {"needToResearch": ""}})
        print(f'Research has been removed in person {personId}')
        result_file.write(f"{personId};REMOVED")

    if not result["needToResearch"]:
        if not result["firstName"] \
                or not result["surname"] \
                or not result["dateOfBirth"] \
                or not result["phone"]:
            uns = db["persons"].update_one({"_id": personId}, {"$set": {"needToResearch": True}})
            print(f'Research has been added in person {personId}')
            result_file.write(f"{personId};ADDED")
result_file.close()

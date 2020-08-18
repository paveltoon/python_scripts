from rldd import rldd2
from user import rldd_user

result = {
    "phone": 0,
    "surname": 0,
    "firstName": 0,
}
result_file = open('res.csv', 'w+')
itera = 0
db = rldd2.DPS_connect(rldd_user.login, rldd_user.pwd)
persons = db["persons"].find({
    "technicalProperties.type": "GOLD"
}, {"surname": 1, "snils": 1, "firstName": 1, "needToResearch": 1, "middleName": 1, "gender": 1, "dateOfBirth": 1,
    "registrationAddressId": 1, "contacts": 1, "identityDocuments": 1})
for person in persons:
    itera += 1
    if itera % 1000 == 0:
        print(itera)

    personId = person["_id"]

    if "needToResearch" in person:
        continue

    if "surname" in person:
        if person["surname"].strip() != '':
            result['surname'] += 1

    if "firstName" in person:
        if person["firstName"].strip() != '':
            result['firstName'] += 1

    if "contacts" in person:
        phoneFound = False
        contacts = person["contacts"]
        for contact in contacts:
            if "type" in contact:
                if contact["type"] == "PHN" or contact["type"] == "MBT":
                    phoneFound = True
        if phoneFound:
            result["phone"] += 1
        else:
            print(personId)
            result_file.write(f'{personId}\n')
result_file.close()
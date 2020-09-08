from rldd import rldd2
from user import rldd_user

result = {
    "snils": 0,
    "surname": 0,
    "firstName": 0,
    "middleName": 0,
    "gender": 0,
    "dateOfBirth": 0,
    "registrationAddressId": 0,
    "emails": 0,
    "phones": 0,
    "docType": 0,
    "docSerial": 0,
    "docNumber": 0,
    "docIssueDate": 0,
    "emailConsent": 0,
    "citizenship": 0,
    "issuePlace": 0,
    "issuePlaceCode": 0,
    "inn": 0,
    "placeOfBirth": 0,
    "locationAddressId": 0,
    "familyStatus": 0,
}
itera = 0
projection = {
    "surname": 1,
    "snils": 1,
    "firstName": 1,
    "needToResearch": 1,
    "middleName": 1,
    "gender": 1,
    "dateOfBirth": 1,
    "registrationAddressId": 1,
    "contacts": 1,
    "identityDocuments": 1,
    "inn": 1,
    "placeOfBirth": 1,
    "locationAddressId": 1,
    "familyStatus": 1,
    "citizenship": 1,
    "agreements.emailConsent": 1,
}
db = rldd2.DPS_connect(rldd_user.login, rldd_user.pwd)
persons = db["persons"].find({
    "technicalProperties.type": "GOLD"
}, projection)

for person in persons:
    itera += 1
    if itera % 10000 == 0:
        print(itera)
    personId = person["_id"]
    if "needToResearch" in person:
        continue
    if "snils" in person:
        result['snils'] += 1

    if "surname" in person:
        if person["surname"].strip() != '':
            result['surname'] += 1
        else:
            print(personId, "Have no surname")

    if "firstName" in person:
        if person["firstName"].strip() != '':
            result['firstName'] += 1

    if "middleName" in person:
        if person["middleName"].strip() != '':
            result['middleName'] += 1

    if "gender" in person:
        if person["gender"].strip() != '':
            result['gender'] += 1

    if "dateOfBirth" in person:
        if person["dateOfBirth"].strip() != '':
            result['dateOfBirth'] += 1

    if "registrationAddressId" in person:
        result['registrationAddressId'] += 1

    if "contacts" in person:
        phoneFound = False
        contacts = person["contacts"]
        for contact in contacts:
            if "type" in contact:
                if contact["type"] == "EML":
                    result["emails"] += 1
                elif contact["type"] == "PHN" or contact["type"] == "MBT":
                    phoneFound = True
        if phoneFound:
            result["phones"] += 1

    if "identityDocuments" in person:
        identityDocuments = person["identityDocuments"]
        for doc in identityDocuments:
            if doc["actual"] and doc['type'] == "PASSPORT":
                result["docType"] += 1
                if "serial" in doc:
                    result["docSerial"] += 1
                if "number" in doc:
                    result["docNumber"] += 1
                if "issueDate" in doc:
                    result["docIssueDate"] += 1
                if "issuePlace" in doc:
                    result["issuePlace"] += 1
                if "issuePlaceCode" in doc:
                    result["issuePlaceCode"] += 1

    if "inn" in person:
        result["inn"] += 1

    if "placeOfBirth" in person:
        result["placeOfBirth"] += 1

    if "locationAddressId" in person:
        result["locationAddressId"] += 1

    if "familyStatus" in person:
        result["familyStatus"] += 1

    if "agreements" in person:
        if "emailConsent":
            result["emailConsent"] += 1

    if "citizenship" in person:
        result["citizenship"] += 1


print('Фамилия;Имя;Отчество;Дата Рождения;Пол;ДУЛ тип;ДУЛ серия;ДУЛ номер;ДУЛ Дата выдчи;Адрес регистрации;Email;Телефон;СНИЛС;Согласие на рассылку;Гражданство;Место выдачи;Код подразделения;ИНН;Место рождения;Фактический адрес (проживания);Семейное положение')
print(f'{result["surname"]};{result["firstName"]};{result["middleName"]};{result["dateOfBirth"]};{result["gender"]};{result["docType"]};{result["docSerial"]};{result["docNumber"]};{result["docIssueDate"]};{result["registrationAddressId"]};{result["emails"]};{result["phones"]};{result["snils"]};{result["emailConsent"]};{result["citizenship"]};{result["issuePlace"]};{result["issuePlaceCode"]};{result["inn"]};{result["placeOfBirth"]};{result["locationAddressId"]};{result["familyStatus"]}')

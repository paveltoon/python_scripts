from rldd.client import Client
from rldd import config

changeList = [
    {
        "ccn": "P001-6158015544-38126563",
        "newTrustedPerson": "13702651133",
        "newPerson": "00140741578"
    }
]

db = Client(config.PROD).connect()
dps = Client(config.DPS, "dps").connect()


def changeTrustedPerson(_ccn, _snils):
    _person = findPerson(_ccn, _snils)
    updater = {
        "trustedPersons.0.trustedPerson.trustedPersonInfo": _person,
        "trustedPersons.0.trustedPerson.trustedId": str(_person["_id"])
    }
    result = setPerson(_ccn, updater)
    return result


def changePerson(_ccn, _snils):
    _person = findPerson(_ccn, _snils)
    updater = {
        "personsInfo.0": _person,
        "person.surname": _person["surname"],
        "person.firstName": _person["firstName"],
        "person.middleName": _person["middleName"],
        "person.applicantType": _person["type"],
        "person.fio": f'{_person["surname"]} {_person["firstName"]} {_person["middleName"]}',
        "persons.0": str(_person["_id"])
    }
    result = setPerson(_ccn, updater)
    return result


def getAddress(_id):
    _address = db["addresses"].find_one({"_id": Client.getId(_id)})
    if "_class" in _address:
        del _address["_class"]
    return _address


def getDoc(_id):
    _doc = db["docs"].find_one({"_id": Client.getId(_id)})
    if "_class" in doc:
        del _doc["_class"]
    return _doc


def setDocsAndAddresses(_person):
    new_person = _person
    if "registrationAddressId" in new_person:
        new_person["registrationAddress"] = getAddress(new_person["registrationAddressId"])

    if "locationAddressId" in new_person:
        new_person["locationAddress"] = getAddress(new_person["locationAddressId"])

    if "ipWorkPlaceAddressId" in new_person:
        new_person["ipWorkPlaceAddress"] = getAddress(new_person["ipWorkPlaceAddressId"])

    if "currIdentityDocId" in new_person:
        new_person["currIdentityDoc"] = getDoc(new_person["currIdentityDocId"])
    return new_person


def findPerson(_ccn, _snils):
    __person = dps["persons"].find_one({"snils": _snils})
    if "_class" in __person:
        del __person["_class"]
    correct_person = setDocsAndAddresses(__person)
    return correct_person


def setPerson(_ccn, updater):
    claim = db["claims"].find_one({"customClaimNumber": _ccn})
    claim_id = claim["_id"]
    upd = db["claims"].update_one({"_id": claim_id}, {"$set": updater})
    return upd


for doc in changeList:
    ccn = doc["ccn"]
    try:
        if "newPerson" in doc:
            if doc["newPerson"] != "":
                person = changePerson(ccn, doc["newPerson"])
                print(ccn, "Person has been corrected")

        if "newTrustedPerson" in doc:
            if doc["newTrustedPerson"] != "":
                trust = changeTrustedPerson(ccn, doc["newTrustedPerson"])
                print(ccn, "Trusted Person has been corrected")
    except TypeError as e:
        print(ccn, e)
        continue

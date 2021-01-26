from rldd.client import Client
from rldd import config


def getAttribute(obj, attr):
    if attr in obj:
        return obj[attr]
    return ""


db = Client(config.DPS, "dps").connect()
persons = db["xxx_dps_persons"].find({})
for person in persons:
    surname = getAttribute(person, "surname")
    firstName = getAttribute(person, "firstName")
    middleName = getAttribute(person, "middleName")
    dateOfBirth = getAttribute(person, "dateOfBirth")
    snils = getAttribute(person, "snils")

    listOfPersons = []

    samePersons = db["xxx_dps_persons"].find({
        "surname": surname,
        "firstName": firstName,
        "middleName": middleName,
        "dateOfBirth": dateOfBirth,
        "snils": snils
    })
    for samePers in samePersons:
        listOfPersons.append(samePers["_id"])

    if len(listOfPersons) > 1:
        pass

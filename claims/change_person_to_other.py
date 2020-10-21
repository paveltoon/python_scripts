from rldd.Person import Person
from rldd.client import Client
from rldd.config import PROD, DPS, DEV

db = Client(PROD).connect()
dps = Client(DPS, "dps").connect()

claims = db["claims"].find(
    {"service.srguServiceId": "1234567891000000001", "persons": {"$ne": "5f85826a2b794559a73bbb1f"}})
person = Person(dps["persons"].find_one({"_id": Client.getId("5f85826a2b794559a73bbb1f")}), db)
person.form_person_to_claim()
full_person = person.get_full_person()
iteration = 0

updater = {
    "persons.0": str(person.get_id()),
    "personsInfo.0": full_person,
    "person": {
        "surname": person.get_attr("surname"),
        "firstName": person.get_attr("firstName"),
        "middleName": person.get_attr("middleName"),
        "applicantType": "PHYSICAL",
        "fio": person.get_fio()
    }
}
for claim in claims:
    claimId = claim["_id"]
    iteration += 1

    db["claims"].update_one({"_id": claimId}, {"$set": updater})
    print(iteration, claimId)

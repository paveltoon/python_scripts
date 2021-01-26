from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
persons = Client(config.DPS, "dps").connect()
result_file = open("fio.csv", "w+")
result_file.write("ФИО;ФИО;id заявки\n")
claims = db["claims"].find({"service.srguServiceId": "5000000000167006500",
                            "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")}})
for claim in claims:
    claim_id = claim["_id"]
    if "personsInfo" not in claim:
        continue

    pers_info = claim["personsInfo"]
    for pers in pers_info:
        pers_id = pers["_id"]
        if "surname" not in pers:
            continue
        person_surname = pers["surname"]
        person = persons["persons"].find_one({"_id": pers_id})
        if person is not None:
            person_surname_orig = person["surname"]
            if person_surname_orig.lower() != person_surname.lower():
                result_file.write(f"{person_surname};{person_surname_orig};{claim_id}\n")
                print(person_surname, person_surname_orig, claim_id)
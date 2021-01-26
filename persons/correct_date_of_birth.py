from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
pers = Client(config.DPS, "dps").connect()

projection = {
    "_id": 1,
    "personsInfo._id": 1,
    "personsInfo.dateOfBirth": 1
}
persons_upd_count = 0
claims_upd_count = 0
persons = pers["persons"].find({"dateOfBirth": {"$regex": "^0.*"}})
for person in persons:
    person_id = person["_id"]
    date_of_birth = person["dateOfBirth"].split("-")
    date_of_birth[0] = "1970"
    new_date = "-".join(date_of_birth)

    person_upd = pers["persons"].update_one({"_id": person_id}, {"$set": {"dateOfBirth": new_date}})
    persons_upd_count += person_upd.modified_count

claims = db["claims"].find({"personsInfo.dateOfBirth": {"$regex": "^0.*"}}, projection)
iterator = 0
for claim in claims:
    iterator += 1
    print(iterator)
    claim_id = claim["_id"]
    personsInfo = claim["personsInfo"]
    for index, pers in enumerate(personsInfo):
        if "dateOfBirth" in pers:

            date_of_birth_claim = pers["dateOfBirth"].split('-')
            date_of_birth_claim[2] = date_of_birth_claim[2].split('T')[0]
            if date_of_birth_claim[0].startswith("0"):
                date_of_birth_claim[0] = "1970"
            claim_upd = db["claims"].update_one(
                {
                    "_id": claim_id
                },
                {"$set":
                    {
                        f"personsInfo.{index}.dateOfBirth": "-".join(date_of_birth_claim)
                    }
                }
            )
            claims_upd_count += claim_upd.modified_count
print(f"Count of corrected persons: {persons_upd_count}")
print(f"Count of corrected claims: {claims_upd_count}")

from rldd.client import Client
from rldd import config
unset_attribute = [
    "surname",
    "firstName",
    "middleName",
    "gender",
    "locationAddressId",
    "dateOfBirth",
    "placeOfBirth",
    "citizenshipCode",
    "registrationAddressId",
    "locationAddressId",
    "registrationAddress",
    "locationAddress",
    "familyStatus",
    "lowerCaseSurname",
    "lowerCaseFirstName",
    "lowerCaseMiddleName",
    "fio",
]
person_attribute = [
    "surname",
    "firstName",
    "middleName",
    "fio"
]
db = Client(config.PROD).connect()
db_persons = Client(config.DPS, "dps").connect()
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-8381225287-39803853",
            "P001-0210301289-39237994",
            "P001-7807221330-39841751"
        ]
    }
})
for claim in claims:
    claim_id = claim["_id"]
    claim_unset_data = {}
    isChanged = False
    person_id = str
    personsInfo = claim["personsInfo"]
    for index, pers in enumerate(personsInfo):
        if pers["type"] == "JURIDICAL":
            person_id = pers["_id"]
            path = f"personsInfo.{index}."
            for atr in unset_attribute:
                if atr in pers:
                    claim_unset_data[path + atr] = ""
                    isChanged = True
        if isChanged:
            claim_person = claim["person"]
            path = f"person."
            for atr in person_attribute:
                if atr in claim_person:
                    claim_unset_data[path + atr] = ""

            claim_Upd = db["claims"].update_one({"_id": claim_id}, {"$unset": claim_unset_data})

            if claim_Upd.modified_count == 1:
                print(f"Claim {claim_id} has been corrected. progress: {claim_Upd.modified_count} / {claim_Upd.matched_count}")
            else:
                print(f"Claim {claim_id} is not modified. progress: {claim_Upd.modified_count} / {claim_Upd.matched_count}")

            person = db_persons["persons"].find_one({"_id": person_id})
            if person is not None:
                person_unset_data = {}
                for atr in unset_attribute:
                    if atr in pers:
                        person_unset_data[atr] = ""
                person_Upd = db_persons["persons"].update_one({"_id": person_id}, {"$unset": person_unset_data})
                if person_Upd.modified_count == 1:
                    print(f"Person {person_id} has been corrected. progress: {person_Upd.modified_count} / {person_Upd.matched_count}")
                else:
                    print(f"Person {person_id} is not modified. progress: {person_Upd.modified_count} / {person_Upd.matched_count}")
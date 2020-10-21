import datetime
import bson
import pymongo

from rldd.client import Client
from rldd import config

dps = Client(config.DPS, "dps").connect()
db = Client(config.PROD).connect()
projection = {
    "_id": 1,
    "lastModified": 1
}
claims_projection = {
    "_id": 1,
    "claimCreate": 1
}
iteration = 0
persons = dps["persons"].find({"technicalProperties.type": "GOLD"}, projection, no_cursor_timeout=True)
for person in persons:
    iteration += 1
    correct_type = None
    person_id = person["_id"]

    if type(person["_id"]) == bson.objectid.ObjectId:
        creation_date = person["_id"].generation_time
        correct_type = "ObjectId"
    elif len(list(db["claims"].find({"persons": str(person["_id"])}, claims_projection).sort("claimCreate", pymongo.ASCENDING))) > 0:
        creation_date = list(db["claims"].find({"persons": str(person["_id"])}, claims_projection).sort("claimCreate", pymongo.ASCENDING))[0]["claimCreate"]
        correct_type = "Claim"
    elif "lastModified" in person:
        creation_date = person["lastModified"]
        correct_type = "lastModified"
    else:
        creation_date = datetime.datetime.now()
        correct_type = "Now"

    upd = dps["persons"].update_one(
        {"_id": person_id},
        {"$set": {"personalDataAgreement.status": True, "personalDataAgreement.date": creation_date}}
    )
    print(f'Iteration: {iteration}. Person {person_id} has been corrected. progress: {upd.modified_count} / {upd.matched_count}. Corrected by {correct_type}.')

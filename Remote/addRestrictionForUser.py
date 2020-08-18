from bson import DBRef, ObjectId

from rldd import rldd2
db = rldd2.REMOTE_connect()
db_list = db.list_database_names()
for dbName in db_list:
    if not dbName.startswith("omsu"):
        continue
    user = db[dbName]["users"].find_one({"login": "andronovaeu"})
    if user is None:
        continue
    userId = user["_id"]
    user_custom_role = user["user_custom_role"]
    for role in user_custom_role:
        if role["staticUR"] == "DEPARTMENTS":
            permissions = role["permissions"]
            permissions.append(DBRef('services', ObjectId('55f1a11c06277ae119998109')))
            upd = db[dbName]["users"].update_one({"_id": userId}, {"$set": {"user_custom_role": user_custom_role}})
            print(dbName, f'{upd.modified_count} / {upd.matched_count}')
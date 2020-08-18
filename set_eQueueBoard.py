from rldd import rldd2
result_file = open("users.csv", "w+")

remote = rldd2.REMOTE_connect()
dbs = remote.list_database_names()
for dbName in dbs:
    if dbName.startswith("mfc"):
        db = remote[dbName]
        users = db["users"].find({ "user_custom_role.staticUR": "OPERATOR" })
        for user in users:
            userId = user["_id"]
            upd = db["users"].update_one({"_id": userId}, {"$set": {"eQueueBoard": True}})
            if upd.modified_count == 1:
                result_file.write(f"{dbName};{userId}\n")
result_file.close()
users.close()
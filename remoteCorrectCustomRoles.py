from bson import DBRef, ObjectId
from rldd import rldd2
from user import rldd_user
import datetime

remoteConn = rldd2.REMOUT_connect()
remoteBases = remoteConn.list_database_names()
for base in remoteBases:
    if base.startswith('mfc'):
        remote = remoteConn[base]
        # USERS
        users = remote["users"].find({"user_custom_role.staticUR": "OPERATOR"})

        for user in users:
            userId = user["_id"]
            user_custom_role = user['user_custom_role']
            for index, role in enumerate(user_custom_role):
                if type(role) is not dict:
                    user_custom_role[index] = role[0]
                    upd2 = remote["users"].update_one({"_id": userId}, {"$set": {"user_custom_role": user_custom_role}})
                    print(f'User {userId} has been updated on base {base}. Progress: {upd2.modified_count} / {upd2.matched_count}')

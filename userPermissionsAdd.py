from bson import DBRef, ObjectId
from rldd import rldd2
from user import rldd_user
import datetime

result_file = open('result.csv', 'w+')
operators_file = open('operators.csv', 'w+')
new_permission = {
    "role": "DEPARTMENTS",
    "permissions": [
        "5000000000213214476"
    ]
}
mfc_permission = {
    "staticUR": "DEPARTMENTS",
    "_id": ObjectId(),
    "version": 0,
    "lastModified": datetime.datetime.now(),
    "permissions": [
        DBRef("services", ObjectId("5ed6699773c2d6a4c3fbbb15"))
    ]
}

# --- Remote Bases ---
count_users = 0
remoteConn = rldd2.REMOUT_connect()
remoteBases = remoteConn.list_database_names()
for base in remoteBases:
    if base.startswith('mfc'):
        remote = remoteConn[base]
        # USERS
        users = remote["users"].find({"user_custom_role.staticUR": "OPERATOR"})

        for user in users:
            isDeparts = False
            count_users += 1
            userId = user["_id"]
            user_custom_role = user["user_custom_role"]
            for role in user_custom_role:
                if 'staticUR' in role:
                    if role['staticUR'] == "DEPARTMENTS":
                        if 'permissions' in role:
                            if not DBRef("services", ObjectId("5ed6699773c2d6a4c3fbbb15")) in role['permissions']:
                                role['permissions'].append(DBRef("services", ObjectId("5ed6699773c2d6a4c3fbbb15")))
                        else:
                            role['permissions'] = []
                            role['permissions'].append(DBRef("services", ObjectId("5ed6699773c2d6a4c3fbbb15")))
                        upd = remote["users"].update_one({"_id": userId}, {"$set": {"user_custom_role": user_custom_role}})
                        print(f'User {userId} has been updated on base {base}. Progress: {upd.modified_count} / {upd.matched_count}')
                        result_file.write(f'{userId};{base}\n')
                        isDeparts = True

            if not isDeparts:
                user_custom_role.append(mfc_permission)
                upd2 = remote["users"].update_one({"_id": userId}, {"$set": {"user_custom_role": user_custom_role}})
                print(f'User {userId} has been updated on base {base}. Progress: {upd2.modified_count} / {upd2.matched_count}')
                result_file.write(f'{userId};{base}\n')

# --- Operators ---
count_operators = 0
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
operators = db['operators'].find({'$and': [{"userPermissions.role": "OPERATOR"},
                                           {"userPermissions.role": {'$ne': "DEPARTMENTS"}},
                                           {"deptId": {'$regex': '^mfc.*'}}]})
for operator in operators:
    count_operators += 1
    operatorId = operator["_id"]
    userPermissions = operator['userPermissions']
    userPermissions.append(new_permission)
    upd3 = db["operators"].update_one({"_id": operatorId}, {"$set": {"userPermissions": userPermissions}})
    print(f'Operator {operatorId} has been updated. Progress: {upd3.modified_count} / {upd3.matched_count}')
    operators_file.write(f'{operatorId}\n')
print('Users', count_users)
print('Operators', count_operators)
result_file.close()
operators_file.close()

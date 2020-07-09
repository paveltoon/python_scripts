import json

from rldd import rldd2
db = rldd2.REMOUT_connect()
user_list = json.load(open('result.json'))

for mfc in user_list:
    users = user_list[mfc]
    users_correct = []
    for user in users:
        users_correct.append(rldd2.getId(user))
    cursor = db[mfc]['users'].update_many({"_id": {"$in": users_correct}}, {"$set": {"eQueueBoard": False}})
    print(mfc, 'Progress:', cursor.modified_count, '/', cursor.matched_count)
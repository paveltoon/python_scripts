from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)

persons = db['persons'].find({"esiaId": {'$exists': True}}, no_cursor_timeout=True)
result_file = open('esiaIds.csv', 'w+')
result_file.write('Person id;Esia id;Update\n')
for person in persons:
    personId = person['_id']
    esiaId = person['esiaId']
    upd = db['persons'].update_one({"_id": personId}, {"$set": {"esia.id": esiaId}})
    result_file.write(f'{personId};{esiaId};{upd.modified_count}/{upd.matched_count}\n')
result_file.close()
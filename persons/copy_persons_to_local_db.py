from rldd import rldd2
from user import rldd_user


def formatSnils(snils_num):
    formatted = snils_num.split('-')
    new_snils = ''.join(formatted).split(' ')
    return ''.join(new_snils)


db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
local = rldd2.LOCAL_connect('local')
persons = db['persons'].find({"snils": {"$regex": '.*-.*'}}).limit(100)
for person in persons:
    snils = person["snils"]
    same_person = db['persons'].find_one({"snils": formatSnils(snils)})
    if same_person is not None:
        local['persons'].save(person)
        local['persons'].save(same_person)
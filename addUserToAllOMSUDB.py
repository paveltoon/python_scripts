from rldd import REMOTE

rem = REMOTE.REMOTE()

db = rem.connect()
db_list = rem.get_db_list()

main_user = db['omsu-reutov']['users'].find_one({"login": "andronovaeu"})

for dbi in db_list:
    if not dbi.startswith('omsu'):
        continue

    if db[dbi]['users'].find_one({"login": "andronovaeu"}) is None:
        ins = db[dbi]['users'].insert_one(main_user)
        print(ins.inserted_id, dbi)
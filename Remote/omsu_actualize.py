from rldd.client import Client
from rldd import config

result_file = open('result.csv', 'w+')
result_file.write(f"dbName;status\n")
dbName_list = open('omsu.txt', 'r+').read().split("\n")
for index, dbName in enumerate(dbName_list):
    db = Client(config.PROD).connect()
    remote = Client(config.REMOTE, dbName).connect()

    orgcard = remote["orgcard"].find_one()

    if orgcard:
        updater = {
            "shortName": orgcard["shortName"]
        }

        upd = db["departments"].update_one({"name": dbName}, {"$set": updater})

        if upd.modified_count:
            result_file.write(f"{dbName};Исправлено\n")
        else:
            result_file.write(f"{dbName};Не исправлено\n")

        print(index + 1, dbName, upd.modified_count)
result_file.close()

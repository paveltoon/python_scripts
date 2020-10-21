from rldd.client import Client
from rldd import config
import datetime

result_file = open('result.csv', 'w+')
result_file.write(f"dbName;status\n")
dbName_list = open('dbs.txt', 'r+').read().split("\n")
for index, dbName in enumerate(dbName_list):
    db = Client(config.PROD).connect()
    remote = Client(config.REMOTE, dbName).connect()

    orgcard = remote["orgcard"].find_one()
    services = remote["services"].find({"serviceIdSrgu": {"$exists": True}})

    if orgcard and services is not None:
        updater = {
            "oktmo": orgcard["oktmo"],
            "name": dbName,
            "shortName": orgcard["armsCaption"],
            "fullName": orgcard["shortName"],
            "email": orgcard["email"],
            "address": orgcard["address"],
            "phone": orgcard["phone"],
            "senderCode": orgcard["senderCode"],
            "srguServiceIds": [],
            "type": "MFC" if dbName.startswith("mfc") else "DEPARTMENT",
            "lastModified": datetime.datetime.now() - datetime.timedelta(hours=3)
        }

        for serv in services:
            if serv["serviceIdSrgu"].strip() != "":
                updater["srguServiceIds"].append(serv["serviceIdSrgu"])

        for key, value in dict(updater).items():
            if value is None:
                del updater[key]

        upd = db["departments"].update_one({"name": dbName}, {"$set": updater}, upsert=True)

        if upd.modified_count or upd.upserted_id:
            result_file.write(f"{dbName};Исправлено\n")
        else:
            result_file.write(f"{dbName};Не исправлено\n")

        print(index + 1, dbName, upd.modified_count, upd.upserted_id)
result_file.close()

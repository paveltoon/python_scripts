from rldd.client import Client
from rldd import config

res_file = open('res.csv', 'w+')
result = ""
db = Client(config.REMOTE, '').connect()
dbNames = db.list_database_names()
for dbName in dbNames:
    if dbName.startswith('mfc'):
        dbServices = Client(config.REMOTE, dbName).connect()
        services = dbServices["services"].find({
            "serviceIdSrgu": {"$in": ["10000018594"]}
        })
        for service in services:
            customFields = service.get("customFields")
            if customFields:
                for field in customFields:
                    if field["field_id"] == "nalog":
                        if field.get("default_value"):
                            result = ";".join([str(dbName), str(service["serviceIdSrgu"]), str(field["default_value"])])
                            res_file.write(result + "\n")
res_file.close()
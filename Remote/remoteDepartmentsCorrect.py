from rldd.client import Client
from rldd.config import REMOTE

dbList = Client(REMOTE, "").connect().list_database_names()
result_file = open("departmentsChanges.csv", "w+")
result_file.write(f"Наименование базы;Id документа;fullName;Изменено\n")


def update_department(_depId, _db):
    _db["departments"].update_one({"_id": _depId}, {"$set": {"deptIdSrgu": "123"}})


for dbName in dbList:
    isCorrected = False
    if dbName.startswith("mfc") or dbName.startswith("omsu"):
        db = Client(REMOTE, dbName).connect()
        departments = db["departments"].find({"fullName": "Органы местного самоуправления"})
        for dep in departments:
            depId = dep["_id"]
            if "deptIdSrgu" in dep:
                if dep["deptIdSrgu"].strip() == "":
                    update_department(depId, db)
                    isCorrected = True
                    result_file.write(f"{dbName};{depId};{dep['fullName']};{isCorrected}\n")
                else:
                    result_file.write(f"{dbName};{depId};{dep['fullName']};{isCorrected}\n")
            else:
                update_department(depId, db)
                isCorrected = True
                result_file.write(f"{dbName};{depId};{dep['fullName']};{isCorrected}\n")

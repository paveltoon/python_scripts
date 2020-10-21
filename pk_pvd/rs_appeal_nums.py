import pymongo
import csv
from rldd.client import Client
iteration = 0
result_file = open('result.csv', 'w+')
result_file.write(f"statements._id;statements.internalNum;orgName;orgCode;name;statements.recordRequisites.recordNum;whenClose;guid_name\n")
with open('pros.csv', newline='') as csvfile:
    file = list(csv.reader(csvfile, delimiter=';', quotechar='|'))
    for row in file:
        iteration += 1
        rs_id = row[1]
        mfc_name = row[0]
        claimNum = row[2]
        result_data = {
            "statements._id": rs_id,
            "statements.internalNum": "",
            "orgName": "",
            "orgCode": "",
            "name": "",
            "statements.recordRequisites.recordNum": "",
            "whenClose": "",
            "guid_name": ""
        }

        client = pymongo.MongoClient("mongodb://pkpvd:ctynz,hm123@10.50.109.227:27017/pvdrs")
        db = client["pvdrs"]

        doc = db["rs_appeal"].find_one({"statements._id": Client.getId(rs_id)})
        if doc:
            appeal_id = doc["_id"]
            for state in doc["statements"]:
                if state["_id"] == Client.getId(rs_id):
                    result_data["statements.internalNum"] = state["internalNum"]
                    if "recordRequisites" in state:
                        if "recordNum" in state["recordRequisites"]:
                            result_data["statements.recordRequisites.recordNum"] = state["recordRequisites"]["recordNum"]

            event = doc["createEvent"]["performer"]
            orgName = event["orgName"]

            if "\n" in orgName:
                orgName = orgName.replace('\n', '')
            if "\r" in orgName:
                orgName = orgName.replace('\r', '')
            if "\t" in orgName:
                orgName = orgName.replace('\t', '')

            result_data["orgName"] = orgName

            result_data["orgCode"] = event["orgCode"]

            result_data["name"] = doc["name"]

            prot = db["prot_IssuedDocument"].find_one({
                "idAppeal": str(appeal_id),
                "currentStep": "ISSUING",
                "oldStep": "PRINT"
            })
            if prot:
                result_data["whenClose"] = prot["whenClose"].isoformat()

            is_doc = list(db["rs_issued_document"].find({
                "statementGuid": rs_id,
                "name": {'$nin': [
                    "Ожидание оплаты",
                    "Сформирована квитанция"
                ]}
            }))

            if len(is_doc) > 0:
                res = []
                for d in is_doc:
                    res.append(d["name"])
                result_data["guid_name"] = ", ".join(res)
            result_string = ""

            for value in result_data.values():
                result_string += value + ';'

            result_file.write(f"{result_string[:-1]}\n")
            print(iteration, result_data)

result_file.close()

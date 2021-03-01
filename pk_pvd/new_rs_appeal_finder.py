import csv
import datetime

from rldd.client import Client
from rldd.config import PKPVD

iteration = 0
db = Client(PKPVD, "pvdrs").connect()
file_in = open('rm.csv', 'r+')
file_out = open('rm_result.csv', 'w+', newline="")
file_out.write(
    "Номер заявления;Наименование процедуры;Текущий статус;Наименование выдаваемого документа;Номер КУВД;Дата отправки на выдачу\n")
csvReader = csv.reader(file_in, delimiter=";")
for row in csvReader:
    iteration += 1
    print(iteration)
    intNum = row[2]
    claim = db["rs_appeal"].find_one({"statements.internalNum": intNum})
    if claim:
        name = claim["name"]
        statusNotePPOZ = claim["statusNotePPOZ"]
        statements = claim["statements"]
        for state in statements:
            if state["internalNum"] == intNum:
                stateId = state["_id"]
                numPPOZ = state["numPPOZ"] if "numPPOZ" in state else ""
                issuedDocs = list(db["rs_issued_document"].find({
                    "statementGuid": str(stateId),
                    "name": {
                        "$nin": [
                            "Сформирована квитанция",
                            "Ожидание оплаты"
                        ]
                    }
                }))
                for issuedDoc in issuedDocs:
                    issuedName = issuedDoc["name"]
                    issuedDocId = issuedDoc["_id"]
                    prots = db["prot_IssuedDocument"].find({
                        "idIssuedDocument": str(issuedDocId),
                        "oldStep": "PRINT",
                        "currentStep": "ISSUING"
                    })
                    for prot in prots:
                        whenClose = datetime.date.strftime(prot["whenClose"], "%d/%m/%Y %H:%M:%S")
                        file_out.write(f"{intNum};{name};{statusNotePPOZ};{issuedName};{numPPOZ};{whenClose}\n")
                        print(f"{intNum};{name};{statusNotePPOZ};{issuedName};{numPPOZ};{whenClose}")

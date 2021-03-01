import pymongo

from rldd.client import Client
from rldd.config import PROD

db = Client(PROD).connect()
result_file = open("services.csv", "w+", newline="")
result_file.write("Наименование услуги;Код процедуры\n")
query = {
    "statusCode": "53",
    "statusDate": {"$gte": Client.ISODate("2019-01-01T00:00:00.000+0000")}
}
total_count = db["claims_status"].count_documents(query)
statuses = db["claims_status"].find(query, no_cursor_timeout=True)
serviceDict = {}
iteration = 0
for status in statuses:
    iteration += 1
    print(f"{iteration} / {total_count}")
    claimId = status["claimId"]
    statusesList = list(db["claims_status"].find({
        "claimId": claimId
    }).sort("statusDate", pymongo.ASCENDING))
    for index, statusElement in enumerate(statusesList):
        if statusElement["statusCode"] == "53":
            if len(statusesList) > index + 1:
                if statusesList[index + 1]["statusCode"] == "2":
                    claim = db["claims"].find_one({"_id": Client.getId(claimId)})
                    if claim:
                        if "service" in claim:
                            try:
                                srguService = claim["service"]["srguServiceId"]
                                srguName = claim["service"]["name"] if "name" in claim["service"] else claim["service"]["srguServiceName"]
                            except KeyError:
                                print(KeyError, claimId)
                                continue
                            if srguService not in serviceDict:
                                serviceDict[srguService] = srguName
                                print(claimId, srguName, srguService)

for key, value in serviceDict.items():
    result_file.write(f"{value};{key}\n")

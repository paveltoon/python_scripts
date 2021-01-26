from rldd.client import Client
from rldd import config
import csv

with open('res.csv', newline='\n') as file:
    bunchOfValues = [row.strip() for row in file]

for row in bunchOfValues:
    fileInfo = row.split(";")
    dbName = fileInfo[0]
    srguId = fileInfo[1]
    defaultValue = fileInfo[2]

    dbServices = Client(config.REMOTE, dbName).connect()
    servicesFromList = dbServices["services"].find({
        "serviceIdSrgu": srguId
    })
    for service in servicesFromList:
        fields = service.get("customFields")
        if fields:
            for field in fields:
                if field["field_id"] == "nalog":
                    if field.get("default_value"):
                        tmpField = field
                        tmpField["default_value"] = defaultValue
                        field = tmpField
                        dbServices["services"].update_one({
                            "serviceIdSrgu": service["serviceIdSrgu"]
                        },
                            {
                                "$set": {
                                    "customFields": fields
                                }
                            })
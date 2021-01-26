from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
query = {"service.srguServiceId": "5000000010000047695",
         "activationDate": {'$gte': Client.ISODate("2020-09-24T21:00:00.000+0000")}
         }

projection = {"_id": 1, "fields": 1, "customClaimNumber": 1, "activationDate": 1}

claims = db["claims"].find(query, projection)
result_file = open('emptyFields.csv', 'w+')
for claim in claims:
    claimId = claim["_id"]
    activationDate = claim["activationDate"]
    ccn = claim["customClaimNumber"] or None
    try:
        if len(claim["fields"]["sequenceValue"]) > 0:
            seq = claim["fields"]["sequenceValue"]
            for elem in seq:
                if "stringId" in elem:
                    if elem["stringId"] == "carList":
                        carList = elem["sequenceValue"]
                        for car in carList:
                            car_data = car["sequenceValue"]
                            for data in car_data:
                                if "stringId" in data:
                                    if data["stringId"] == "carBrands":
                                        if not len(data["sequenceValue"]):
                                            print(ccn, "carBrands")
                                            result_file.write(f"{ccn};{activationDate};carBrands\n")
                                    if data["stringId"] == "carModels":
                                        if not len(data["sequenceValue"]):
                                            print(ccn, "carModels")
                                            result_file.write(f"{ccn};{activationDate};carModels\n")
    except KeyError as k:
        print(claimId, k)
        result_file.write(f"{ccn};{k}\n")
result_file.close()

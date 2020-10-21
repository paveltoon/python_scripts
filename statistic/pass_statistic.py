from rldd.client import Client
from rldd import config

result_file = open('result_stat.csv', 'w+')
srguList = []
db = Client(config.PROD).connect()
statuses = db["claims_status"].find(
    {
        "statusCode": {'$in': ["47", "84"]},
        "statusDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")}
    }
)


def getAttribute(obj, attr):
    if attr in obj:
        return obj[attr]
    return None


for status in statuses:
    claimId = Client.getId(status["claimId"])
    claim = db["claims"].find_one({"_id": claimId})
    if claim:

        if "service" in claim:
            result_str = ""
            service = claim["service"]
            if getAttribute(service, "srguServiceId") not in srguList:
                srguList.append(getAttribute(service, "srguServiceId"))
                obj = {"srguServiceId": getAttribute(service, "srguServiceId"),
                       "srguServiceName": getAttribute(service, "srguServiceName"),
                       "srguServicePassportId": getAttribute(service, "srguServicePassportId"),
                       "srguServicePassportName": getAttribute(service, "srguServicePassportName"),
                       "srguDepartmentId": getAttribute(service, "srguDepartmentId"),
                       "srguDepartmentName": getAttribute(service, "srguDepartmentName")}
                for value in obj.values():
                    result_str += value + ';'
                result_file.write(f"{result_str[:-1]}\n")
result_file.close()
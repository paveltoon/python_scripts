from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({
    "service.srguServicePassportId": "5000000000193224739",
    "senderCode": {'$regex': "^50000.*"},
    "activationDate": {"$gte": Client.ISODate("2020-10-11T21:00:00.000+0000"),
                       "$lte": Client.ISODate("2020-10-12T21:00:00.000+0000")}
})
result_file = open("zahoron.csv", "w+")
result_file.write("наименование МФЦ;наименование процедуры;ФИО заявителя;дата подачи;статус;дата проставления статуса\n")
for claim in claims:
    ccn = claim["customClaimNumber"]
    curr = claim["currStatus"]
    result = {
        "dept": claim["creatorDeptId"],
        "srgu": claim["service"]["name"],
        "fio": claim["person"]["fio"],
        "actDate": claim["activationDate"].isoformat(),
        "statusCode": curr["statusCode"],
        "statusDate": curr["statusDate"].isoformat()
    }

    isSecond = False
    isSix = False

    if "statuses" in claim:
        for status in claim["statuses"]:
            if status["statusCode"] == "2":
                isSecond = True
            if status["statusCode"] == "6":
                isSix = True

    if not isSecond and isSix:
        result_str = ""
        for key, value in result.items():
            result_str += value + ";"
        result_file.write(result_str[:-1] + "\n")

import csv
import datetime

from rldd.client import Client
from rldd import config
db = Client(config.PROD).connect()
res_file = open("res.csv", "w+")
res_file.write(f"Номер;Дата подачи;Дата закрытия;Статусы;Статус дедлайна;Дней до дедлайна;\n")
with open('milk.csv', newline='', encoding="utf-8") as file:
    claims = csv.reader(file, delimiter=';')
    for row in claims:
        ccn = row[0]
        claim = db["claims"].find_one({"customClaimNumber": ccn})
        if claim is None:
            print(f"{ccn};NO CLAIM;;;\n")
            continue
        try:
            daysToDeadline = claim["daysToDeadline"]
            claimId = claim["_id"]
            claimCreate = claim["claimCreate"]
            resultStatus = claim["resultStatus"]
            docSendDate = claim["docSendDate"]
            deadlineStatus = str
            if int(daysToDeadline) < 0:
                deadlineStatus = "BAD"
            else:
                deadlineStatus = "OK"
        except KeyError as k:
            print(f"No key {k} in claim {ccn}")

        print(ccn)

        if datetime.datetime(2019, 12, 1) <= claimCreate <= datetime.datetime(2020, 1, 9):
            if docSendDate < datetime.datetime(2020, 1, 28):
                statuses = db["claims_status"].find({"claimId": str(claimId)})
                st_list = []
                for status in statuses:
                    if status["statusCode"] == "34" or status["statusCode"] == "53":
                        st_list.append(status["statusCode"])
                if "34" in st_list and "53" in st_list:
                    res_file.write(f"{ccn};;;OK;{deadlineStatus};{daysToDeadline}\n")
                else:
                    res_file.write(f"{ccn};;;BAD;{deadlineStatus};{daysToDeadline}\n")
            else:
                res_file.write(f"{ccn};;{docSendDate};;{deadlineStatus};{daysToDeadline}\n")
        else:
            res_file.write(f"{ccn};{claimCreate};;;{deadlineStatus};{daysToDeadline}\n")

import csv
from datetime import timedelta
from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
iterat = 0
file_num = 0
result_file = open(f"./files/mku_new_{file_num}.csv", "w+")


def getActualDate(date):
    new_date = date + timedelta(hours=3)
    r = {
        "year": new_date.year,
        "month": new_date.month,
        "day": new_date.day,
        "hour": new_date.hour,
        "minute": new_date.minute,
        "second": new_date.second
    }

    for d in r:
        if r[d] < 10:
            r[d] = f"0{r[d]}"

    return f'{r["day"]}-{r["month"]}-{r["year"]} {r["hour"]}:{r["minute"]}:{r["second"]}'


with open('../deadlines_correct.csv', newline='') as file:
    reader = csv.reader(file, delimiter=";")
    for row in reader:
        iterat += 1
        ccn = row[0]
        claim = db["claims"].find_one({"customClaimNumber": ccn})
        if claim:
            claimId = claim["_id"]
            print(f"{claimId};{getActualDate(claim['deadlineDate'])}")
            result_file.write(f"{claimId};{getActualDate(claim['deadlineDate'])}\n")

        if iterat % 150000 == 0:
            file_num += 1
            result_file.close()
            result_file = open(f"./files/mku_new_{file_num}.csv", "w+")
result_file.close()

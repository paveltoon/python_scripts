from datetime import datetime, timedelta
from rldd import rldd2
from user import rldd_user


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


iterat = 0
file_num = 1
result_file = open(f"./files/mku_new_{file_num}.csv", "w+")
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims_status_mku"].find({"statusDate": rldd2.ISODate("2020-10-01T21:00:00.000+0000")})
for claim in claims:

    iterat += 1
    claimId = claim["claimId"]
    print(f"{claimId};{getActualDate(claim['statusDate'])}")
    result_file.write(f"{claimId};{getActualDate(claim['statusDate'])}\n")

    if iterat % 150000 == 0:
        file_num += 1
        result_file.close()
        result_file = open(f"./files/mku_new_{file_num}.csv", "w+")
result_file.close()

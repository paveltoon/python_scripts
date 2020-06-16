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

    return f'{r["year"]}-{r["month"]}-{r["day"]} {r["hour"]}:{r["minute"]}:{r["second"]}'

iter = 0
file_num = 1
result_file = open(f"./files/mku_new_{file_num}.csv", "w+")
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
claims = db["claims"].find({"deadlineDate": rldd2.ISODate("2020-07-13T21:00:00.000+0000")})
for claim in claims:

    iter += 1
    claimId = claim["_id"]
    print(f"{claimId};{getActualDate(claim['deadlineDate'])}")
    result_file.write(f"{claimId};{getActualDate(claim['deadlineDate'])}\n")

    if iter % 150000 == 0:
        file_num += 1
        result_file.close()
        result_file = open(f"./files/mku_new_{file_num}.csv", "w+")
result_file.close()

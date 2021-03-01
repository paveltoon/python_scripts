import datetime

from rldd.client import Client
from rldd.config import PKPVD


def format_date(_date):
    return datetime.date.strftime(_date, "%d/%m/%Y %H:%M:%S")


pvd = Client(PKPVD, "pvdrs").connect()
result_file = open("rejects_suspenses.csv", "w+", newline="")
result_file.write(
    "ID обращения;Номер обращения;Номер PKPVDMFC;Дата подачи;Дата приостановки;Кол-во приостановок;Дата отказа;Кол-во отказов;Регистрационные действия\n")
messages = pvd["jrnl_ppozinmessage"].find({
    "statusWhen": {
        "$gte": Client.ISODate("2020-06-09T21:00:00.000+0000"),
        "$lte": Client.ISODate("2020-12-31T21:00:00.000+0000")
    },
    "statusCode": {"$in": ["suspended", "rejected"]}
})
iteration = 0
for message in messages:
    iteration += 1
    rejects = 0
    suspense = 0
    try:
        substanceId = message["substanceId"]
        requestNumber = message["requestNumber"]
    except KeyError:
        continue
    rejectsWhen = []
    suspensesWhen = []
    docs = pvd["jrnl_ppozinmessage"].find({
        "statusWhen": {
            "$gte": Client.ISODate("2020-06-09T21:00:00.000+0000"),
            "$lte": Client.ISODate("2020-12-31T21:00:00.000+0000")
        },
        "statusCode": {"$in": ["suspended", "rejected"]},
        "substanceId": substanceId
    })

    for doc in docs:
        if doc["statusCode"] == "suspended":
            suspense += 1
            suspensesWhen.append(format_date(doc["statusWhen"]))
        if doc["statusCode"] == "rejected":
            rejects += 1
            rejectsWhen.append(format_date(doc["statusWhen"]))

    appeal = pvd["rs_appeal"].find_one({"_id": substanceId})
    internalNum = appeal["internalNum"] if "internalNum" in appeal else ""
    name = appeal["name"] if "name" in appeal else ""
    dateWhen = format_date(appeal["createEvent"]["dateWhen"])
    print(iteration, substanceId, rejects, suspense)
    result_file.write(
        f"{substanceId};{internalNum};{requestNumber};{dateWhen};{', '.join(suspensesWhen)};{suspense};{', '.join(rejectsWhen)};{rejects};{name}\n")

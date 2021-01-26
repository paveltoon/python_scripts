from rldd.client import Client
from rldd import config
import csv


def format_snils(_snils):
    newForm = "".join(_snils.split("-"))
    return "".join(newForm.split(" ")).strip()


dps = Client(config.DPS, "dps").connect()

in_file = open("soc_id.csv", newline="")
reader = csv.reader(in_file, delimiter=";")
next(reader, None)
iteration = 0
for row in reader:
    iteration += 1
    snils = row[0]
    person = dps["xxx_rpgu_persons"].find_one({"socialId": snils})
    if person:
        upd = dps["xxx_rpgu_persons"].update_one({"_id": person["_id"]}, {
            "$set": {
                "messagesCount": row[1]
            }
        })
        print(iteration, person["_id"], upd.modified_count)
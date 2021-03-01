import csv

from rldd.client import Client
from rldd import config


def formatSnils(snils_num):
    formatted = snils_num.split('-')
    new_snils = ''.join(formatted).split(' ')
    return ''.join(new_snils)


db = Client(config.DPS, "dps").connect()
in_file = open("ac.csv", "r+")
reader = csv.reader(in_file, delimiter=";")
next(reader, None)

for row in reader:
    snils = formatSnils(row[0])
    esiaId = row[1]
    esiaType = row[2]
    person = db["persons"].find_one({"snils": snils})
    if person:
        upd = db["persons"].update_one(
            {
                "_id": person["_id"]
            }, {
                "$set": {
                    "esia.id": esiaId,
                    "esia.authorizationType": esiaType
                }
            }
        )
        print(f"Person {person['_id']} {upd.modified_count} / {upd.matched_count}")

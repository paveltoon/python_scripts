from rldd.client import Client
from rldd import config
import csv
dps = Client(config.DPS, "dps").connect()
iteration = 0
with open('snilses.csv') as csvfile:
    snilses_list = list(csv.reader(csvfile, delimiter=';', quotechar='|'))[1434301:]
    for snils in snilses_list:
        iteration += 1
        person = dps["persons"].find_one({"snils": snils[0]})

        if person:
            personId = person["_id"]
            upd = dps["persons"].update_one({"_id": personId}, {"$set": {"esiaAutorisation": True}})
            print(f'{iteration}. {personId}, {upd.modified_count} / {upd.matched_count}')

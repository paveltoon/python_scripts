import csv
from rldd.client import Client
from rldd import config

dps = Client(config.DPS, 'dps').connect()["persons"]
db = Client(config.PROD).connect()
res_file = open('data.csv', 'w+')
iteration = 0
with open('data2.csv') as csv_file:
    file = csv.reader(csv_file, delimiter=',')
    for row in file:
        iteration += 1
        personId = row[2]
        person = dps.find_one({"_id": Client.getId(personId)})

        print(iteration, personId)
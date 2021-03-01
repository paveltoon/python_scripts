from bson import InvalidBSON

from rldd.client import Client
from rldd import config

dps = Client(config.DEV).connect()

iteration = 0
while True:
    try:
        persons = dps["claims"].find().limit(10).skip(iteration)
        for person in persons:
            iteration += 1
            print(person)
        break
    except InvalidBSON as e:
        iteration += 1
        print(e)
        continue

from rldd.client import Client
from rldd import config


class Person:
    def __init__(self, __person_id):
        self.person_id = __person_id

    def get_person(self):
        db = Client(config.DPS, "dps").connect()
        person = db["persons"].find_one({"_id": Client.getId(self.person_id)})
        return person

from rldd.client import Client
from rldd import config


class Address:
    def __init__(self, __address_id):
        self.__address_id = __address_id

    def get_address(self):
        db = Client(config.PROD).connect()
        address = db["addresses"].find_one({"_id": Client.getId(self.__address_id)})
        return address

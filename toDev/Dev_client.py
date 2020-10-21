from rldd.client import Client
from rldd import config


class Dev_client(Client):
    def __init__(self, conf, data_base="rldd2"):
        Client.__init__(self, conf, data_base)
        self.db = Client(conf, data_base).connect()

    def get_element(self, collection, element_id):
        element = self.db[collection].find_one({"_id": element_id})
        return element

    def return_result(self):
        pass

from toDev.Dev_client import Dev_client
from rldd import config
import pymongo


class Status(Dev_client):
    def __init__(self, conf, data_base, __claim_id):
        Dev_client.__init__(self, conf, data_base)
        self.__claim_id = __claim_id

    def get_statuses(self):
        return self.get_element("claims_status", self.__claim_id)

    def get_element(self, collection, element_id):
        statuses = self.db[collection].find({"claimId": element_id}).sort("statusDate", pymongo.ASCENDING)
        return statuses


newDev = Status(config.PROD, "rldd2", )

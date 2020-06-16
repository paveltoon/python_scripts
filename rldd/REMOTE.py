import pymongo
from rldd.Main import Main


class REMOTE(Main):
    __url = '10.10.80.100:27017'

    def connect(self):
        clients = pymongo.MongoClient(f"mongodb://{self.__url}")
        return clients

    def get_db_list(self):
        return self.connect().list_database_names()


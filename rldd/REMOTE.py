import pymongo
from rldd.Main import Main


class REMOTE(Main):
    __url = '10.10.80.100:27017'

    def connect(self):
        client = pymongo.MongoClient(f"mongodb://{self.__url}")
        return client

    def get_db_list(self):
        return self.connect().list_database_names()


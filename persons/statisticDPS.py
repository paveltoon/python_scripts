import pymongo
from user import rldd_user

client = pymongo.MongoClient(f'mongodb://{rldd_user.login}:{rldd_user.pwd}@eisgmu-dps-db-01:27017/dps', )
db = client["dps"]
persons = db['persons'].find({"technicalProperties.type": "GOLD", "surname": {'$exists': True}})


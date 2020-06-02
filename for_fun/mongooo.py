import pymongo
client = pymongo.MongoClient('mongodb://192.168.0.182:27017/')
db = client.get_database('test')
test = db['test'].find({})
for t in test:
    print(t['customClaimNumber'])
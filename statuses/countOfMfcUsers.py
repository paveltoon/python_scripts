from rldd.client import Client
from rldd import config

replica = Client(config.replicaSET, "mfc-objects-replication").connect()
replicaData = replica["dbs-info"].find({"dbType": "OMSU"})
iteration = 0
mfcUsersCount = 0
for rep in replicaData:
    dbName = rep["dbName"]
    remote = Client(config.REMOTE, dbName).connect()
    usersCount = remote["users"].count_documents({"$or": [{"isDeleted": False}, {"isDeleted": {"$exists": False}}]})
    mfcUsersCount += usersCount
print(mfcUsersCount)

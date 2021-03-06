from rldd.client import Client
from rldd import config
from deadlines.deadline_functions import setDeadlineToOneDay

db = Client(config.PROD).connect()
claimsFile = open("claimIds.txt")
claimsList = claimsFile.read().split("\n")
for claimId in claimsList:
    setDeadlineToOneDay({"_id": Client.getId(claimId), "resultStatus": {"$exists": True}})

from rldd.client import Client
from rldd import config

dps_dev = Client(config.DPS_DEV, 'dps-develop').connect()
dps = Client(config.DPS, 'dps').connect()

dpsDocs = dps_dev["analytics"].find({
    "esiaVerificationWidget.interactionDate": {
        "$gte": Client.ISODate("2021-02-04T15:30:00.000+0000")
    }
})

inserts = dps["analytics"].insert_many(dpsDocs)
print(inserts.inserted_ids)

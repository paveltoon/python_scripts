from rldd.client import Client
from rldd import config

dps = Client(config.DPS, "dps").connect()
phoneNumber = "9636699888"


def parseNumber(_num):
    pass

# dps["persons"].find({ "contacts.value": "+7(963)6699888" })

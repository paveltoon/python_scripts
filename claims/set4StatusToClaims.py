from rldd.client import Client
from rldd import config

client = Client(config.PROD)
db = client.connect()
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-3206060485-38442141",
            "P001-8777633930-38669048",
            "P001-9035191347-38490792",
            "P001-5550349546-38279361",
            "P001-7334602401-38578180",
            "P001-8378983642-38458407",
            "P001-8378983642-38458894",
            "P001-0457096026-38774976",
            "P001-4370267090-38372832",
            "P001-3884170601-38462274",
            "P001-5205403179-38268679",
            "P001-8875649947-38575415",
            "P001-0257828240-38288922",
            "P001-0536022742-39473316",
            "P001-0798303238-39175168",
            "P001-4500273732-38567354",
            "P001-5026543613-38648596",
            "P001-1973411847-38281729",
            "P001-3240530790-39270122",
            "P001-9033133783-39136489"
        ]
    }
})
for claim in claims:
    client.postStatus(claim["_id"], 4, "")

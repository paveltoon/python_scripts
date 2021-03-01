from bson import ObjectId

from rldd.client import Client
from rldd import config

client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-1383261447-25274100",
            "P001-8308318634-31609007",
            "P001-8176945817-30071582",
            "P001-9451094602-22471215"
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 24, "")

    print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration} \n {response.text.encode('utf-8')}")

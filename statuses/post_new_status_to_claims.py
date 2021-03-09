from bson import ObjectId

from rldd.client import Client
from rldd import config

client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-9411085075-42403100"
        ]
    }
}
)
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 4, "")

    print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration} \n {response.text.encode('utf-8')}")

from rldd.client import Client
from rldd import config

client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "M508-9983452244-41830590"
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 1, "")

    print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration} \n {response.text.encode('utf-8')}")

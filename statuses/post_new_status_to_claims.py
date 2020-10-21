from rldd.client import Client
from rldd import config

tasknum = "EISOUSUP-6308"
client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-6565202428-39316125"
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 2, f"Статус проставлен автоматически через РЛДД.")

    print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration} \n {response.text.encode('utf-8')}")

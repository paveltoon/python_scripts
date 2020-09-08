from rldd.client import Client
from rldd import config

tasknum = "EISOUSUP-6183"
client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "P001-8868538896-38021696",
            "P001-7893140004-38024472",
            "P001-4039428943-38069146",
            "P001-3338405505-38111282"
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 6, f"Статус проставлен автоматически через РЛДД, в рамках задачи {tasknum}.")

    print(f"Claim {claimId} is done. Iteration: {iteration} \n {response.text}")

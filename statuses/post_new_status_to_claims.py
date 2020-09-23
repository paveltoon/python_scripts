from rldd.client import Client
from rldd import config

tasknum = "SD-2246"
client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "customClaimNumber": {
        "$in": [
            "M509-2970938781-35616001",
            "M509-5935131017-35613751",
            "M509-7251327160-35613005",
            "M509-0690720555-35609682",
            "M509-8751000684-35603843",
            "M509-8655186395-35603092",
            "M509-8327301193-35597172",
            "M509-1441138460-35595796"
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    response = client.postStatus(claimId, 24, f"Статус проставлен автоматически через РЛДД, в рамках задачи {tasknum}.")

    print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration} \n {response.text.encode('utf-8')}")

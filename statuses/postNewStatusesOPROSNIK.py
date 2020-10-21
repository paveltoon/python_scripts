from rldd.client import Client
from rldd import config

client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({"service.srguServiceId": "1234567890000000001", "currStatus.statusCode": "2",
                            "claimCreate": {'$gte': Client.ISODate("2020-01-08T16:19:26.860+0000")}})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    status62 = False
    client.postStatus(claimId, 56, "Статус проставлен автоматически через РЛДД")
    client.postStatus(claimId, 3, "Статус проставлен автоматически через РЛДД")
    # client.postStatus(claimId, 62, "Статус проставлен автоматически через РЛДД, в рамках задачи EISOUSUP-6074")

    while not status62:
        statuses = db["claims_status"].find_one({"claimId": str(claimId), "statusCode": "62"})
        if statuses is not None:
            status62 = True
            client.postStatus(claimId, 24, "Статус проставлен автоматически через РЛДД")

    print(f"Claim {claimId} is done. Iteration: {iteration}")

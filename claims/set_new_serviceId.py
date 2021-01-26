from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()

services = [
    {
        "old_code": "5000000000186926857",
        "new_code": "5000000000186896269"
    },
    {
        "old_code": "5000000000193194152",
        "new_code": "5000000000193194144"
    },
    {
        "old_code": "5000000000217809934",
        "new_code": "5000000000217809933"
    },
    {
        "old_code": "5000000000217809937",
        "new_code": "5000000000217809936"
    },
    {
        "old_code": "5000000000217810058",
        "new_code": "5000000000217810057"
    },
    {
        "old_code": "5000000000217810060",
        "new_code": "5000000000217810059"
    },
    {
        "old_code": "5000000000217810062",
        "new_code": "5000000000217810061"
    },
]

for code in services:
    old_code = code["old_code"]
    new_code = code["new_code"]

    count = db["claims"].update_many(
        {"service.srguServiceId": old_code},
        {"$set": {
            "service.srguServiceId": new_code
        }}
    )
    print(f"С кода: {old_code} на код {new_code} изменено {count.modified_count} заявок.")

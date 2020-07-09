from rldd import rldd2
from pymongo.errors import InvalidBSON
db = rldd2.DEV_connect()

processed = 0
while True:
    try:
        claims = db["claims"].find({}).limit(100).skip(processed)
        for claim in claims:
            print(claim["_id"])
            processed += 1
        break
    except InvalidBSON as e:
        print(e)
        processed += 1

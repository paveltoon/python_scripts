from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
result_file = open('pushevent.csv', 'w+')
claims = db["claims"].find({"service.srguServiceId": "5000000000216071966", "statuses.1": {'$exists': False},
                            "claimCreate": {'$gte': rldd2.ISODate("2020-07-04T21:00:00.000+0000")}})
for claim in claims:
    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]

    pushEvent = db["int_push_events"].find({"event.claimId": str(claimId), "recipient": "EISZVPOO"})
    for event in pushEvent:
        if 'attempts' in event:
            eventId = event["_id"]
            upd = db["int_push_events"].update_one({"_id": eventId}, {"$set": {"status": "NOT_READY", "attempts": 0}})

            result_file.write(f'{str(claimId)};{upd.modified_count}\n')
            print(f'Event for claim {str(claimId)} has been updated. progress: {upd.modified_count} / {upd.matched_count}')
        else:
            result_file.write(f'{str(claimId)};0\n')
            print(f'Have no event for claim {claimId}')
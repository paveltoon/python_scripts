from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
upd = db["int_push_events"].update_many({"status": "NOT_READY_NO_MORE_ATTEMPTS", "recipient": "EISZVPOO"},
                                        {"$set": {"status": "SENT"}})
print(f'{upd.modified_count} / {upd.matched_count}')

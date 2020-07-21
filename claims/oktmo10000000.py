from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
db['claims'].update_many(
    {"oktmo": "10000000", "currStatus.deptId": {"$exists": False}}, {
        '$set': {
            "oktmo": "46000000"
        }})

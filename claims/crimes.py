from bson import ObjectId
import datetime
from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({"service.srguServiceId": "5000000000184561111", "resultStatus": {'$exists': False}})

iteration = 0

pre_integration_file = open("pre.csv", "w+")
pre_integration_file.write("claim id;Дата(МСК)\n")
post_integration_file = open("post.csv", "w+")
post_integration_file.write("claim id;Дата(МСК)\n")


def insert_status(_status_num, _claim_id):
    _status = {
        "_id": ObjectId(),
        "claimId": str(_claim_id),
        "statusCode": str(_status_num),
        "statusDate": datetime.datetime.now(),
        "lastModified": datetime.datetime.now(),
        "createBy": "rldd2",
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED",
        "createDate": datetime.datetime.now(),
        "_class": "status"
    }
    upd = db["claims_status"].insert_one(_status)
    return upd.inserted_id


def add_status_into_claim(_status, _claim_id):
    _status_to_body = db["claims_status"].find_one({"_id": _status})
    del _status_to_body["_class"]
    del _status_to_body["claimId"]
    del _status_to_body["lastModifiedBy"]
    del _status_to_body["createBy"]
    del _status_to_body["lastModified"]
    del _status_to_body["createDate"]
    upd = db["claims"].update_one({"_id": _claim_id}, {"$push": {"statuses": _status_to_body}})
    return upd


def set_result(_claim_id, _date):
    upd = db['claims'].update_one({"_id": _claim_id}, {"$set": {"resultStatus": "3", "docSendDate": _date}})
    return upd


def get_status(_status_id):
    st = db["claims_status"].find_one({"_id": _status_id})
    return st


for claim in claims:
    iteration += 1
    claim_id = claim["_id"]
    claim_create = claim["claimCreate"]

    status_id = insert_status(3, claim_id)
    status = get_status(status_id)

    claim_status_arr = add_status_into_claim(status_id, claim_id)

    result = set_result(claim_id, status["statusDate"])

    if claim_create < datetime.datetime(2020, 4, 23, 19, 30):
        pre_integration_file.write(f'{claim_id};{claim_create + datetime.timedelta(hours=3)}\n')
    else:
        post_integration_file.write(f'{claim_id};{claim_create + datetime.timedelta(hours=3)}\n')

    print(iteration, claim_id, "Corrected")

from rldd.client import Client
from rldd import config
import csv

client = Client(config.PROD)
db = client.connect()
remote_client = Client(config.REMOTE, '')
db_list = remote_client.get_db_list()
remote = remote_client.connect()


def get_service__attributes(_service: dict, _name: str, _id_name: str, _id_value: str):
    if _name not in _service:
        _claim = db["claims"].find_one({
            f"service.{_id_name}": _id_value,
            f"service.{_name}": {"$exists": True}
        })
        if _claim:
            _result = {
                f"service.{_name}": _claim["service"][_name]
            }
            if _id_name not in _service:
                _result[f"service.{_id_name}"] = _id_value
            return _result


with open('kz.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=";")
    next(reader, None)
    for row in reader:
        ccn = row[0]
        srguServiceId = row[3]
        departmentId = row[5]
        srguPassportId = row[7]
        new_status: str = row[8]
        # if new_status.strip() == "":
        #     continue

        claim = db["claims"].find_one({"customClaimNumber": ccn})
        if claim:
            # if "currStatus" in claim:
            #     continue
            # claim_id = claim["_id"]
            # statuses = db["claims_status"].find_one({"claimId": str(claim_id)})
            # if statuses:
            #     continue
            # response = client.postStatus(str(claim_id), new_status, "")
            # print(new_status, response.text)
            if "service" in claim:
                service = claim["service"]
                updater = {}
                names = [
                    get_service__attributes(service, "name", "srguServiceId", srguServiceId),
                    get_service__attributes(service, "srguServicePassportName", "srguServicePassportId",
                                            srguPassportId),
                    get_service__attributes(service, "srguDepartmentName", "srguDepartmentId", departmentId)
                ]
                for obj in names:
                    if obj is not None:
                        updater = {**updater, **obj}

                        upd = db["claims"].update_many({"customClaimNumber": ccn}, {
                            "$set": updater
                        })
                        print(f"Claim {ccn}, {upd.modified_count} / {upd.matched_count}")

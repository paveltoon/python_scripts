from rldd.Main import Main
from user import rldd_user

import json
import requests
import pymongo


class PROD(Main):
    login = rldd_user.login
    password = rldd_user.pwd
    url = "10.10.80.54:8080"

    def connect(self, db_name="rldd2"):
        client = pymongo.MongoClient(f"mongodb://{self.login}:{self.password}@10.10.80.31:27017/rldd2")
        return client[db_name]

    def postStatus(self, claim_id, status_code,
                   comment="Статус создан автоматически через РЛДД, для корректного закрытия заявки."):
        url = f'http://{self.url}/api/statuses/'
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "claimId": str(claim_id),
            "statusCode": str(status_code),
            "createBy": "rldd2",
            "comment": comment,
            "lastModifiedBy": "rldd2",
            "createState": "COMPLETED"
        }
        return requests.request("POST", url=url, headers=headers, data=json.dumps(body))

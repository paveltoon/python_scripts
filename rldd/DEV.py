from rldd.Main import Main
import json
import requests
import pymongo


class DEV(Main):
    login = "rlddService"
    password = "1q2w3e4r"
    url = "10.10.80.20"

    def connect(self):
        client = pymongo.MongoClient(f"mongodb://{self.login}:{self.password}@{self.url}:27018/rldd2")
        return client["rldd2"]

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

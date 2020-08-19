from rldd import rldd2
from requests import request
import json
from user import rldd_user
import pandas as pd
import os.path
desktop = os.path.expanduser('~/Desktop')
result_file = open(f'{desktop}\\addStatus.log', 'w+')
statusesURL = 'http://10.10.80.20/api/statuses/'
headers = {
    'Content-type': 'application/json'
}
db = rldd2.DEV_connect()
file = pd.read_csv('test.csv', encoding='utf-8', sep=';')
for index, row in file.iterrows():
    ccn = row['ccn']
    claim = db['claims'].find_one({"customClaimNumber": ccn})
    if claim is not None:
        _id = claim["_id"]
        status = row["status"]
        comment = row["comment"]
        payload = {
            "claimId": str(_id),
            "statusCode": str(status),
            "createBy": "rldd2",
            "comment": str(comment),
            "lastModifiedBy": "rldd2",
            "createState": "COMPLETED"
        }
        response = request("POST", statusesURL, headers=headers, data=json.dumps(payload))
        print(response.text.encode('utf-8'))
        if 200 <= int(response.status_code) <= 300:
            result_file.write(f'{ccn} was added {status} status.\n')
    else:
        print(f'Claim {ccn} not found.')
        result_file.write(f'Claim {ccn} not found.\n')
result_file.close()

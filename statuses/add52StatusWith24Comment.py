import pymongo
import requests
import json

from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)


def postStatus(_claim_id, _status_code, _comment, _sender_code):
    url = 'http://10.10.80.54:8080/api/statuses/'

    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "claimId": str(_claim_id),
        "statusCode": str(_status_code),
        "senderCode": str(_sender_code),
        "comment": _comment,
        "createState": "COMPLETED"
    }
    return requests.request("POST", url=url, headers=headers, data=json.dumps(body))


claimsArr = [
    "P001-0307532046-15971891",
    "P001-4984407758-36780483",
    "P001-2042099641-36763222",
    "P001-2798847815-36789948",
    "P001-1959457395-36825100",
    "P001-9844212550-36853561",
    "A001-3253934531-36862541",
    "P001-1033092920-36886797",
    "P001-5123378267-36894977",
    "P001-4062235074-36895669",
    "P001-2055162945-36902763",
    "P001-2141596744-36906429",
    "P001-2651841160-36907017",
    "P001-1858898060-36918751",
    "P001-8224781348-36921149",
    "P001-8818373814-36926995",
    "P001-1056551168-36937672",
    "P001-8148308794-36939758",
    "P001-2753094072-36945300",
    "P001-3910656302-36947146",
    "P001-9647923335-36948103",
    "P001-6026698907-36953597",
    "P001-0771894851-36953568",
    "P001-8362071181-36955296",
    "P001-5222005662-36957697",
    "P001-4367324531-36965015",
    "P001-2481632095-36972061",
    "P001-9251492491-36974904",
    "P001-1122606236-36976725",
    "P001-0622003908-36986491",
    "P001-2306194596-36989021",
    "P001-4563843873-36989555",
    "P001-4940048799-36989532",
    "P001-1834251863-37000725",
    "P001-6485495810-37002046",
    "P001-6672825858-37003248",
    "P001-4748797956-37006039",
    "P001-6590876876-37010205",
    "P001-9113691772-37011369",
    "P001-5976701204-37017401",
    "P001-4328766994-37019541",
    "P001-9905144582-37026257",
    "P001-4065287136-37027855",
    "P001-0967532603-37031129",
    "P001-0967532603-37031337",
    "P001-0967532603-37031289",
    "P001-0396152924-37035421",
    "P001-5845032652-37038894",
    "P001-7003920067-37044043",
    "P001-2254518403-37047385",
    "P001-8220986668-37057158",
    "P001-4854914146-37064095",
    "P001-5458830688-37064305",
    "P001-9935248578-37072651",
    "P001-1333709363-36934740",
    "P001-6485495810-37002217",
    "P001-8159384588-37079041",
    "P001-2733139492-37121815"
]

claims = db['claims'].find({"customClaimNumber": {'$in': claimsArr}})
for claim in claims:
    claimId = claim['_id']
    isFound = False
    comment = str
    senderCode = str
    statuses = db['claims_status'].find({"claimId": str(claimId)}).sort("statusDate", pymongo.DESCENDING)
    for status in statuses:
        if status['statusCode'] == '24':
            comment = status['comment']
            senderCode = status['senderCode']
            isFound = True
            break
    if isFound:
        newStatus = postStatus(claimId, 52, comment, senderCode)
        print(newStatus.text.encode('utf-8'))
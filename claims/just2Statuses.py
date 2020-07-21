from user import rldd_user
from rldd import rldd2
import json
import requests
import pymongo

claimsId = [
    "9cab9f6d-51a4-4a26-95d8-c78d4786baf5",
    "57f046f0-d69a-439d-9aad-ee0b5c4d6859",
    "0d8b67de-10f8-4f25-94b9-bed9410773d4",
    "e8187484-7e82-46a7-90f2-3309e6a1eb6a",
    "c1e46968-d1fd-45ef-95c7-0d28dd6b8912",
    "41ed8a8b-2a79-4981-8f53-8275c9b585be",
    "75c9dafd-7e48-427a-af26-b4cb73820f75",
    "e79dd9a1-943f-45f1-adbd-9eb628849a07",
    "e3fa7837-957d-42b9-88ba-f285864a40f1",
    "75903c3a-361a-4735-a36c-c842e6d8a77b",
    "7cf453a1-c33b-418e-806c-7dda16a9be57",
    "0439548c-1dab-4c75-8164-85a133195e26",
    "e27a0faf-3855-4b33-a427-3536a4ab9306",
    "da436386-95b7-40df-bb74-1ff6db6fc356",
    "5efee3c022e5c6000183e5c8",
    "5efeefc922e5c60001846652",
    "5efeef9622e5c60001846403",
    "5efeed7d22e5c60001844edb",
    "5efee53522e5c6000183f7a7",
    "5efeef3f22e5c60001846129",
    "5efef03922e5c60001846c13",
    "5efef1f922e5c60001847e4e",
    "5efeebb222e5c60001843bba",
    "5efeeebc22e5c60001845bab",
    "5efee6e922e5c60001840abc",
    "5efeea2422e5c60001842b43",
    "5efee23022e5c6000183d629",
    "5efee88e22e5c60001841b9c",
    "5efee8b222e5c60001841c02",
    "5efef21522e5c60001847f80",
    "5efeef1022e5c60001845f8d",
    "5efee97622e5c600018424af",
    "5efee51f22e5c6000183f61b",
    "5efeedb622e5c6000184516b",
    "5efeed5c22e5c60001844df0",
    "5efeed2422e5c60001844b62",
    "5efef17322e5c6000184780c",
    "5efef0a322e5c600018470bb",
    "5efef15022e5c60001847737",
    "5efeeb1b22e5c6000184342e",
    "5efeeea222e5c60001845af6",
    "5efeecd822e5c600018447fb",
    "5efef05822e5c60001846d39",
    "5efef04322e5c60001846cbb",
    "5efee78922e5c60001841001",
    "5efee6f722e5c60001840b28",
    "5efd0fc922e5c60001875adb",
    "5efef1f622e5c60001847e31",
    "5efee50322e5c6000183f58e",
    "5efeedbf22e5c600018451d6",
    "5efee11822e5c6000192b3d9",
    "5efef1a622e5c60001847acb",
    "5efeee7d22e5c60001845a43",
    "5efeed9322e5c60001844f8e",
    "5efee5b022e5c6000183fe45",
    "5efef19722e5c60001847a0f",
    "5efeecda22e5c60001844806",
    "5efef1fb22e5c60001847e70",
    "5efd92b722e5c60001895958",
    "5efef03522e5c60001846be6",
    "5efef14322e5c60001847707",
    "5efef25e22e5c60001848261",
    "5e60d2ff22e5c60001d96385",
    "5efee34822e5c6000183e290",
    "5efeeafa22e5c600018432cf",
    "5efef13b22e5c60001847662",
    "5efeecb222e5c600018445f7",
    "5efee70722e5c60001840b81",
    "5efee97122e5c60001842498",
    "5efee56122e5c6000183f9fe",
    "5efef25322e5c60001848227",
    "5efeeb3822e5c60001843576",
    "5efee50e22e5c6000183f59f",
    "5efee7b522e5c6000184120f",
    "5efeedf422e5c600018454b2",
    "5efef1db22e5c60001847cc1",
    "5efeec0522e5c60001843ee3",
    "5efee33f22e5c6000183e213",
    "5efee1a322e5c6000183cfb1",
    "5efeedcc22e5c60001845337",
    "5efef09422e5c60001846f9b",
    "5efeef4e22e5c600018461cd",
    "5efeea9a22e5c60001842f70",
    "5efee6d722e5c60001840aa2",
    "5efee43422e5c6000183e9ff",
    "5efee59622e5c6000183fc5a",
    "5efeee2422e5c6000184568b",
    "5edb607622e5c600012d7bf7",
    "5efef15122e5c60001847771",
    "5efeee7422e5c600018459d9",
    "5efeed5022e5c60001844d88",
    "5efee9f222e5c600018428fe",
    "5efee90622e5c60001842125",
    "5efee70522e5c60001840b6c",
    "5efeec6722e5c60001844225",
    "5efef25022e5c6000184820b",
    "5efee32422e5c6000183e0af",
    "5efef1e222e5c60001847d13",
    "5efee9c722e5c600018427cf",
    "5efef19e22e5c60001847a76",
    "5efef13a22e5c60001847658",
    "5ecb853422e5c60001da9ead",
    "5efef0de22e5c6000184729b",
    "5efee9e222e5c60001842899",
    "5e7870f122e5c600017299eb",
    "5efeed4f22e5c60001844d74",
    "5efeea1422e5c60001842978",
    "5efee6b222e5c60001840963",
    "5efee91722e5c60001842145",
    "5efeef4c22e5c600018461b0",
    "5efee2cf22e5c6000183ddc4",
    "5efee42b22e5c6000183e9c5",
    "5efee34422e5c6000183e253",
    "5efef04322e5c60001846c99",
    "5efee40722e5c6000183e92d",
    "5efee29722e5c6000183daac",
    "5ebea27b22e5c60001d5c6d2",
    "5efeede422e5c600018453ef",
    "5eba630322e5c60001c22948",
    "5efee48722e5c6000183eee8",
    "5efeea8b22e5c60001842f07",
    "5efef08d22e5c60001846ed6"
]
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
for claim in claimsId:
    cursor = db["claims"].find_one({"_id": rldd2.getId(claim), "currStatus.statusCode": "2"})
    if cursor is not None:
        claimId = cursor["_id"]
        statuses = db["claims_status"].find({"claimId": str(claimId)}).sort("statusDate", pymongo.ASCENDING)
        prevStatus = None
        for status in statuses:
            statusCode = status["statusCode"]
            if prevStatus is None:
                prevStatus = statusCode
                continue
            if prevStatus != "2" and prevStatus != "1" and statusCode == "2":
                print(claim)
                print(prevStatus)
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {
                    "claimId": str(claimId),
                    "statusCode": prevStatus,
                    "createBy": "rldd2",
                    "comment": "Статус создан автоматически через РЛДД, для корректного закрытия заявки",
                    "lastModifiedBy": "rldd2",
                    "createState": "COMPLETED"
                }
                res = requests.post('http://10.10.80.54:8080/api/statuses', headers=headers, data=json.dumps(data))
                print(res.text.encode('utf-8'))
            prevStatus = statusCode

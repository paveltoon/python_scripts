import json

import requests
from bson import ObjectId

from rldd.client import Client
from rldd import config


def postStatus(claim_id, status_code, _senderCode, _senderName):
    url = 'http://10.10.80.54:8080/api/statuses/'

    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "claimId": str(claim_id),
        "statusCode": str(status_code),
        "createBy": "rldd2",
        "senderCode": _senderCode,
        "senderName": _senderName,
        "lastModifiedBy": "rldd2",
        "createState": "COMPLETED"
    }
    return requests.request("POST", url=url, headers=headers, data=json.dumps(body))


client = Client(config.PROD)
db = client.connect()
iteration = 0
claims = db["claims"].find({
    "_id": {
        "$in": [
            ObjectId("6026375f6844440001f8d6fb"),
            ObjectId("6026806a6844440001fdd979"),
            ObjectId("602685746844440001fe3d64"),
            ObjectId("602817ce684444000104df57"),
            ObjectId("60281892684444000104e132"),
            ObjectId("60282f76684444000105116d"),
            ObjectId("6028dba5684444000105e1ab"),
            ObjectId("6028f0666844440001061d65"),
            ObjectId("60293b06684444000106f77d"),
            ObjectId("602942c56844440001070ffe"),
            ObjectId("602952716844440001073c87"),
            ObjectId("602a2d5d68444400010aa5d1"),
            ObjectId("602a369968444400010b408c"),
            ObjectId("602a4ef968444400010cb791"),
            ObjectId("602a58e768444400010d53b4"),
            ObjectId("602a5b4a68444400010d7dd9"),
            ObjectId("602a638368444400010e037e"),
            ObjectId("602a76eb68444400010f315f"),
            ObjectId("602a7ed968444400010fb0e5"),
            ObjectId("602a89ff6844440001104b43"),
            ObjectId("602aae81684444000111af40"),
            ObjectId("602aaf5e684444000111b516"),
            ObjectId("602ab6e5684444000111e1a3"),
            ObjectId("602abb31684444000111f84b"),
            ObjectId("602ac9c168444400011243fd"),
            ObjectId("602ad7c26844440001127ef5"),
            ObjectId("602ae116684444000112bf24"),
            ObjectId("602ae124684444000112bfa9"),
            ObjectId("602ae126684444000112bfc4"),
            ObjectId("602ae127684444000112bfd3"),
            ObjectId("602ae159684444000112bff7"),
            ObjectId("602ae1c4684444000112c061"),
            ObjectId("602ae1ee684444000112c0c0"),
            ObjectId("602ae23f684444000112c223"),
            ObjectId("602ae254684444000112c23d"),
            ObjectId("602ae299684444000112c287"),
            ObjectId("602ae2ba684444000112c2df"),
            ObjectId("602ae376684444000112c524"),
            ObjectId("602ae3a1684444000112c542"),
            ObjectId("602ae3db684444000112c57a"),
            ObjectId("602ae411684444000112c5c7"),
            ObjectId("602ae438684444000112c608"),
            ObjectId("602ae51c684444000112c7fb"),
            ObjectId("602ae54f684444000112c838"),
            ObjectId("602ae5e3684444000112c9e3"),
            ObjectId("602ae605684444000112ca11"),
            ObjectId("602ae66f684444000112cad5"),
            ObjectId("602ae699684444000112caea"),
            ObjectId("602ae71b684444000112cc8d"),
            ObjectId("602ae7b1684444000112cdb4"),
            ObjectId("602ae88b684444000112cefe"),
            ObjectId("602aea3e684444000112d1ad"),
            ObjectId("602aea63684444000112d22e"),
            ObjectId("602aeba0684444000112d3e0"),
            ObjectId("602aec56684444000112d485"),
            ObjectId("602aecfc684444000112d606"),
            ObjectId("602aed81684444000112d67b"),
            ObjectId("602aeedc684444000112d8ba"),
            ObjectId("602aef3e684444000112d9cf"),
            ObjectId("602aef48684444000112d9de"),
            ObjectId("602af140684444000112dc13"),
            ObjectId("602af1b1684444000112dd23"),
            ObjectId("602af3af684444000112df86"),
            ObjectId("602af3f3684444000112dfba"),
            ObjectId("602af463684444000112dfec"),
            ObjectId("602afadd684444000112e67e"),
            ObjectId("602b59496844440001136d08"),
            ObjectId("602b6b3a6844440001144989"),
            ObjectId("602b8eab684444000116b49a"),
            ObjectId("602b8fe3684444000116c687"),
            ObjectId("602b998168444400011777c1"),
            ObjectId("602b9b6a6844440001179904"),
            ObjectId("602b9edc684444000117d0e4"),
            ObjectId("602ba8626844440001187b33"),
            ObjectId("602bb4a36844440001196ecd"),
            ObjectId("602bde9b68444400011c8863"),
            ObjectId("602be8ec68444400011d04e0"),
            ObjectId("602bea0668444400011d108c"),
            ObjectId("602bf1ef68444400011d6155"),
            ObjectId("602c03e768444400011e0342"),
            ObjectId("602c04a168444400011e0760"),
            ObjectId("602c08f668444400011e239e"),
            ObjectId("602c0bd668444400011e38b2"),
            ObjectId("602c266a68444400011ede99"),
            ObjectId("602c2ad468444400011f4eb4"),
            ObjectId("602c326968444400011fa882"),
            ObjectId("602c329d68444400011fa917"),
            ObjectId("602c32f568444400011fa98d"),
            ObjectId("602c334768444400011faa2b"),
            ObjectId("602c336068444400011faa76"),
            ObjectId("602c336a68444400011faa8d"),
            ObjectId("602c33e268444400011fac2e"),
            ObjectId("602c340b68444400011fac6a"),
            ObjectId("602c348a68444400011fad0c"),
            ObjectId("602c34ae68444400011fad48"),
            ObjectId("602c34b068444400011fad73"),
            ObjectId("602c34de68444400011fae76"),
            ObjectId("602c34e368444400011fae8a"),
            ObjectId("602c34f368444400011fae9f"),
            ObjectId("602c34fb68444400011faebf"),
            ObjectId("602c350a68444400011faee8"),
            ObjectId("602c353768444400011faf22"),
            ObjectId("602c357868444400011faf74"),
            ObjectId("602c357968444400011faf83"),
            ObjectId("602c35ae68444400011fafe5"),
            ObjectId("602c35c068444400011fb00f"),
            ObjectId("602c35d468444400011fb054"),
            ObjectId("602c35f068444400011fb148"),
            ObjectId("602c360368444400011fb188"),
            ObjectId("602c361268444400011fb1bf"),
            ObjectId("602c364b68444400011fb227"),
            ObjectId("602c365d68444400011fb23b"),
            ObjectId("602c369e68444400011fb2ca"),
            ObjectId("602c36dd68444400011fb30d"),
            ObjectId("602c36f868444400011fb32a"),
            ObjectId("602c370f68444400011fb3a0"),
            ObjectId("602c371268444400011fb3d4"),
            ObjectId("602c375a68444400011fb4e0"),
            ObjectId("602c386e68444400011fb6e6"),
            ObjectId("602c388168444400011fb6fb"),
            ObjectId("602c389768444400011fb71f"),
            ObjectId("602c38d368444400011fb7d2"),
            ObjectId("602c38fe68444400011fb810"),
            ObjectId("602c391968444400011fb84b"),
            ObjectId("602c393368444400011fb871"),
            ObjectId("602c396e68444400011fb90d"),
            ObjectId("602c39bc68444400011fb9d5"),
            ObjectId("602c39d868444400011fb9f8"),
            ObjectId("602c3a3468444400011fba75"),
            ObjectId("602c3aa468444400011fbb63"),
            ObjectId("602c3ac768444400011fbbac"),
            ObjectId("602c3ade68444400011fbbbd"),
            ObjectId("602c3b3c68444400011fbbe4"),
            ObjectId("602c3b6f68444400011fbc39"),
            ObjectId("602c3b7368444400011fbc56"),
            ObjectId("602c3c3368444400011fbe11"),
            ObjectId("602c3cc668444400011fbe93"),
            ObjectId("602c3cea68444400011fbf13"),
            ObjectId("602c3dc868444400011fc03d"),
            ObjectId("602c3e0e68444400011fc07f"),
            ObjectId("602c3e2268444400011fc12b"),
            ObjectId("602c3e3668444400011fc194"),
            ObjectId("602c3e8768444400011fc1d4"),
            ObjectId("602c3f4668444400011fc256"),
            ObjectId("602c3fdb68444400011fc38a"),
            ObjectId("602c400068444400011fc3c3"),
            ObjectId("602c40a068444400011fc4f8"),
            ObjectId("602c40b068444400011fc52c"),
            ObjectId("602c417d68444400011fc59a"),
            ObjectId("602c41c268444400011fc684"),
            ObjectId("602c41cb68444400011fc694"),
            ObjectId("602c430368444400011fc824"),
            ObjectId("602c437368444400011fc883"),
            ObjectId("602c437668444400011fc893"),
            ObjectId("602c438e68444400011fc8a2"),
            ObjectId("602c43b068444400011fc8dd"),
            ObjectId("602c43d168444400011fc90b"),
            ObjectId("602c447b68444400011fca80"),
            ObjectId("602c44b668444400011fcab2"),
            ObjectId("602c44f268444400011fcad7"),
            ObjectId("602c467668444400011fcce4"),
            ObjectId("602c46a168444400011fcd0f"),
            ObjectId("602c471d68444400011fcd3e"),
            ObjectId("602c471d68444400011fcd51"),
            ObjectId("602c478b68444400011fce27"),
            ObjectId("602c47b368444400011fce98"),
            ObjectId("602c480768444400011fceaf"),
            ObjectId("602c4abf68444400011fd19c"),
            ObjectId("602c4b0668444400011fd230"),
            ObjectId("602c4e0268444400011fd4f8"),
            ObjectId("602c510e68444400011fd807"),
            ObjectId("602c595368444400011fe55b"),
            ObjectId("602c5a9f68444400011fe693"),
            ObjectId("602cc42b684444000121cfc9"),
            ObjectId("602ccba068444400012259d2")
        ]
    }
})
for claim in claims:
    iteration += 1
    claimId = claim["_id"]
    status = db["claims_status"].find_one({"claimId": str(claimId), "statusCode": "2"})
    if status:
        senderCode = status["senderCode"]
        senderName = status["senderName"]

        response = postStatus(claimId, 2, senderCode, senderName)

        print(f"{iteration}. Claim {claimId} is done. Iteration: {iteration}")

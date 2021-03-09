from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()

passportIds = [
    "5000000000195779559",
    "5000000000163644128",
    "5000000000166988901",
    "5000000000182658694",
    "5000000010000093105",
    "5000000010000093165",
    "5000000010000094640",
    "5000000000195368979",
    "5000000000167006307",
    "5000000000175379417",
    "5000000000182664035",
    "5000000000184861616",
    "5000000000188307694",
    "5000000000167180326",
    "5000000000188204311",
    "5000000000179232903",
    "5000000000179929941",
    "5000000000179337644",
    "5000000000192022708",
    "5000000000195801282",
    "5000000000195835288",
    "197169926",
    "5000000000196515252",
    "5000000000196515252",
    "196905308",
    "197140857",
    "5000000000166983489",
    "196383415",
    "372713547",
    "5000000000216393320",
    "10000060591",
    "5000000000199139982",
    "5000000000212226371",
    "5000000000212278463",
    "5000000000196396439",
    "5000000000196414181",
    "5000000000213944971",
    "5000000000197443124",
    "5000000000188550737",
    "5000000000167012390",
    "5000000000181151220",
    "5000000000166993815",
    "5000000000192267759",
    "5000000000185893654",
    "5000000000185899190",
    "5000000000175406124",
    "5000000000185790834",
    "5000000000167012390",
    "5000000000185899190",
    "5000000000186557838",
    "5000000010000002807",
    "5000000010000002810",
    "5000000000182799258",
    "5000000010000008509",
    "5000000010000002815",
    "5000000000178113091",
    "5000000000214404335",
    "5000000000177914050",
    "5000000000178112908",
    "5000000000178113239",
    "5000000000178047496",
    "5000000000167003647",
    "5000000000186738601",
    "5000000000178113202",
    "5000000000186836729",
    "5000000000186843536",
    "5000000000186738673",
    "5000000000166999894",
    "5000000000167107798",
    "5000000010000052393",
    "5000000000197484426",
    "5000000000196793213",
    "5000000000196795211",
    "5000000000196302121",
    "5000000000214278344",
    "5000000000214404335",
    "5000000000184667175",
    "5000000000185787336",
    "5000000000195751781",
    "5000000000196513029",
    "5000000010000004664",
    "5000000010000097401",
    "5000000000166986702",
    "5000000000167433775",
    "5000000000189808193",
    "5000000000160299214",
    "5000000000196394746",
    "5000000000196928854",
    "5000000000185986199",
    "5000000010000009318",
    "5000000000195326753",
    "5000000000216000436",
    "5000000010000033577",
    "5000000010000012336",
    "5000000000190120455",
    "5000000010000065387",
    "5000000010000005742",
    "5000000010000003636",
    "5000000000222231851",
    "5000000010000003636",
    "5000000010000003763",
    "5000000010000000510",
    "5000000000179701565",
    "5000000010000099911",
    "5000000000183629984",
    "5000000000223698088",
    "5000000000222800688",
    "5000000000181317403",
    "5000000010000015441",
    "5000000000160302593",
    "188083107",
    "5000000000186719768",
    "5000000000183970738",
    "5000000000185452616",
    "5000000000184762039",
    "5000000000188087510",
    "5000000000186719768",
    "5000000000196509120",
    "5000000010000047449",
    "5000000010000091643",
    "5000000000194553144",
    "5000000000183970738",
    "5000000000216804234",
    "5000000000194551092",
    "5000000010000188082",
    "5000000000184722959",
    "5000000000185675394",
    "5000000000195445622",
    "5000000010000069942",
    "5000000010000127598",
    "5000000000000000099",
    "5000000000196923257",
    "5000000000197074155",
    "5000000010000201341",
    "5000000010000201330",
    "5000000010000201338",
    "188083107"
]

for passportId in passportIds:
    rpguDocs = db["claims"].count_documents({
        "activationDate": {
            "$gte": Client.ISODate("2020-12-31T21:00:00.000+0000"),
            "$lte": Client.ISODate("2021-01-31T21:00:00.000+0000")
        },
        "service.srguServicePassportId": passportId,
        "senderCode": "IPGU01001"
    })
    allDocs = db["claims"].count_documents({
        "activationDate": {
            "$gte": Client.ISODate("2020-12-31T21:00:00.000+0000"),
            "$lte": Client.ISODate("2021-01-31T21:00:00.000+0000")
        },
        "service.srguServicePassportId": passportId,
    })
    print(f"{rpguDocs};{allDocs}")
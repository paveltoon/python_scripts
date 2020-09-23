from bson import DBRef

from rldd.client import Client
from rldd import config

srgus = [
    "5000000000178054582",
    "5000000000178054581",
    "5000000000178525415",
    "5000000000186877898",
    "5000000000167027271",
    "5000000000183656898_999",
    "5000000000178113247",
    "5000000000178054586",
    "5000000000178054585",
    "5000000000178054584",
    "5000000000178054583",
    "5000000000201227634",
    "5000000000178112927_999",
    "5022200010000005384",
    "5000000000186841621",
    "5000000000166988150",
    "5000000000166706962",
    "5000000000167243491",
    "5000000000166986093",
    "5000000000179646854",
    "5000000000167002198001",
    "5000000000179232384",
    "5000000000167002198_999",
    "5000000010000052422",
    "5000000000181330461",
    "5000000000183656898",
    "5000000000178113099",
    "2044",
    "5000000000183657046_888",
    "5000000000166999955",
    "5000000000186218384_999",
    "100005486",
    "5000000000167108494",
    "5000000000178112694_999",
    "5000000000186845030",
    "5000000000187041192",
    "5000000000179644704",
    "5000000000167137912",
    "5000000000179642687009",
    "5000000000188564713111",
    "5000000000167006500",
    "5000000000167000520",
    "5000000000179724207",
    "5000000000186890241",
    "5000000000186896269999",
    "5000000000179646168",
    "5000000010000215650",
    "5000000000167014179",
    "5000000010000004434",
    "5000000000186877898_999",
    "5000000000182799268001",
    "66666666",
    "5000000000167003717",
    "5000000000212332981",
    "5025800010000008290",
    "5000000010000004435",
    "5000000000178113099_999",
    "5000000000178112927",
    "5000000000184774934",
    "5000000000167000854",
    "5000000000180180850",
    "5000000000179646311",
    "5000000000178112613_999",
    "5000000000166706959",
    "5000000000167000108009",
    "5000000000167249680",
    "50000000001797242072",
    "50000000001797242071",
    "5000000000186878759",
    "5000000000167322907",
    "5000000000166993997",
    "5000000000186848326",
    "15000000000167137912",
    "5000000000187025820",
    "5000000000186218384",
    "5000000000188563714111",
    "5000000000167000181",
    "5000000000184774926",
    "5000000000179646824",
    "5000000000183657046",
    "5000000000160297449",
    "5000000000167063427",
    "5000000000179649014",
    "5000000000166988752",
    "5000000000167006371",
    "5000000000167000006_999",
    "5000000000193481097",
    "5000000000187042508",
    "5000000000180180741_999",
    "5000000000167013866",
    "5000000000186847245",
    "5000000000184819392",
    "5040100010000046630",
    "5000000000167004236",
    "5000000000182799268",
    "5000000000167014828",
    "5000000000179343642",
    "5000000000167006379",
    "5000000000167028205",
    "5000000000184774950",
    "000000",
    "5000000000166988987",
    "5000000000178053985",
    "5000000000179734845",
    "5000000000167008969",
    "5000000000188175664",
    "5000000000179645950",
    "5000000000187042508_999",
    "5000000000167247088",
    "5000000000181330388",
    "5000000000179648891",
    "5000000000185452655",
    "5000000000185452657",
    "5000000000185452659",
    "5000000000166985940",
    "5000000000167000528",
    "5025300010000006781",
    "5000000000167012998",
    "5000000000183657046_999",
    "5000000000167641566_999",
    "5000000000167012512",
    "5000000000178053985_999",
    "5000000000180766588",
    "5000000000167013567",
    "5000000000178112857",
    "5000000000185452652",
    "5000000000178112613",
    "5000000000186945881",
    "5000000000179648816",
    "5000000000179646511",
    "5000000000167108627",
    "5000000000187025820_999",
    "177475139",
    "5000000000181151306",
    "5000000000177520692",
    "5000000000167250195",
    "5000000000187791137",
    "5000000000183630507",
    "5000000000184029106",
    "5000000000167009075",
    "5000000000183670204",
    "5000000000186879242_999",
    "5000000000180766632",
    "5000000000185452661",
    "5000000000178524658",
    "809643488",
    "5000000000179646904",
    "5000000000182648309",
    "500000000017973484502",
    "5000000000188182646",
    "500000000017973484501",
    "5000000000166983876",
    "5000000000179648923",
    "5000000000192339504",
    "5000000000166983874",
    "1170875645",
    "5000000000179232370",
    "5000000000178113247_999",
    "5000000000186879242",
    "5000000000179232373",
    "5000000000179232374",
    "5000000000167000108",
    "5000000000179232371"
]
permissions = []
rem = Client(config.REMOTE, "omsu-roshal").connect()
op = Client(config.PROD).connect()
operator = op["operators"].find_one({})
user = rem["users"].find_one({"login": "minstroi"})
user_id = user["_id"]
services = rem["services"].find({"serviceIdSrgu": {'$in': srgus}})
for serv in services:
    permissions.append(DBRef('services', serv["_id"]))
for index, role in enumerate(user["user_custom_role"]):
    if role["staticUR"] == "OBSERVER":
        upd_u = rem["users"].update_one({"_id": user_id}, {"$set": {f"user_custom_role.{index}.permissions": permissions}})
        print(upd_u.modified_count, upd_u.matched_count)
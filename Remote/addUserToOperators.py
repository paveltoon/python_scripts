from bson import DBRef, ObjectId
from rldd import rldd2
from user import rldd_user

remote = rldd2.REMOUT_connect()
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
db_list = remote.list_database_names()
for dbName in db_list:
    if dbName.startswith('omsu'):
        operators = db['operators'].find_one({"username": "andronovaeu", "deptId": dbName})
        if operators is None:
            try:
                orgcard = remote[dbName]['orgcard'].find_one({})
                oktmo = orgcard['oktmo']

                new_user = {
                    "_id": ObjectId(),
                    "fio": "Андронова Екатерина Юрьевна ",
                    "oktmo": oktmo,
                    "username": "andronovaeu",
                    "userPermissions": [
                        {
                            "role": "DEPARTMENTS",
                            "permissions": [
                                "5000000000167008969",
                                "5000000000188485829_999",
                                "5000000000188485829",
                                "5000000000167009075",
                                "5000000000166983874",
                                "5000000000197085807",
                                "5000000000197085805"
                            ]
                        },
                        {
                            "role": "OBSERVER",
                            "permissions": [
                                "5000000000186877898",
                                "5000000000183656898_999",
                                "5000000000181628456",
                                "5000000000178113247",
                                "5000000000188180114",
                                "5022200010000005384",
                                "5000000000166988150",
                                "5000000000166706962",
                                "5000000000166986093",
                                "5000000000167002198001",
                                "5000000000188288374",
                                "5000000000179232384",
                                "5000000000188206729",
                                "5000000000192267033",
                                "5000000000181330461",
                                "5000000000183656898",
                                "5000000000166999955",
                                "100005486",
                                "5000000000188206859_999",
                                "5000000000186845030",
                                "5000000010000024338",
                                "5000000000187041192",
                                "5000000000179644704",
                                "5000000010000009076",
                                "5000000000188295228",
                                "5000000000167006500",
                                "5000000000167000520",
                                "5000000000171684896",
                                "5000000000180934640",
                                "66666666",
                                "50000000100",
                                "5000000010000008755",
                                "5000000000189194517",
                                "5000000000179857348",
                                "5000000000178113099_999",
                                "5000000000178112927",
                                "5000000000184774934",
                                "5000000000167000854",
                                "5000000000180180850",
                                "5000000000179646311",
                                "5000000000192267744",
                                "5000000000166706959",
                                "5000000000167000108009",
                                "5000000000167249680",
                                "5000000000190509724",
                                "5000000000185450961_999",
                                "5000000000186878759",
                                "5000000000166993997",
                                "5000000000186848326",
                                "5000000000184099791",
                                "5000000000185450961",
                                "5000000000187025820",
                                "5000000000167000181",
                                "5000000000188183414",
                                "5000000000184774926",
                                "5000000000188288364",
                                "5000000000183657046",
                                "5000000010000068293",
                                "5000000000160297449",
                                "5000000000167063427",
                                "5000000000179649014",
                                "5000000000167006371",
                                "5000000000181309671",
                                "5000000000188295268",
                                "5000000000180180741_999",
                                "5000000000182799268",
                                "5000000000179343642",
                                "5000000000167006379",
                                "5020400010000028755123",
                                "5000000000184774950",
                                "000000",
                                "5000000000167641566",
                                "5000000000184099813",
                                "5000000010000001436",
                                "5000000000178053985",
                                "5000000000179734845",
                                "5000000000188183289",
                                "5000000000188175664",
                                "5000000000187042508_999",
                                "5000000000167247088",
                                "5000000000181330388",
                                "5000000010000028445",
                                "5000000000185452655",
                                "5000000000185452657",
                                "5000000000185452659",
                                "5040100010000002237",
                                "5000000000183657046_999",
                                "5000000000181628555",
                                "5000000000180766588",
                                "5000000000167013567",
                                "5000000000178112857",
                                "5000000000185452652",
                                "5000000000178112613",
                                "50000000001798573481",
                                "5000000000179648816",
                                "5000000000179646511",
                                "5000000000167108627",
                                "5000000000187025820_999",
                                "177475139",
                                "5000000000181151306",
                                "5000000000180253039",
                                "5000000000187791137",
                                "5000000000181309662",
                                "5000000000183630507",
                                "5000000000167009075",
                                "5000000000186879242_999",
                                "5000000000185452661",
                                "5000000000178524658",
                                "5000000000188182646",
                                "5000000000179648923",
                                "5000000000178113247_999",
                                "5000000000186879242",
                                "5000000000192266047",
                                "5000000000192023964",
                                "5000000000178054582",
                                "5000000000178054581",
                                "5000000000178525415",
                                "5000000000186847789000",
                                "5000000000171684833",
                                "5000000000167027271",
                                "5000000000178054586",
                                "5000000000178054585",
                                "5000000000178054584",
                                "5000000000178054583",
                                "5000000000188485829",
                                "5000000000178112927_999",
                                "5000000000186841621",
                                "5000000000187025890",
                                "5000000000179646854",
                                "5000000000181317537",
                                "5000000000192540131",
                                "5000000010000181255",
                                "5000000000178113099",
                                "2044",
                                "5000000000183657046_888",
                                "5000000000168988723",
                                "5000000000186218384_999",
                                "5000000000167108494",
                                "5000000000167137912",
                                "5000000000179642687009",
                                "5000000000181319163",
                                "5000000000187050618",
                                "5000000000167000006",
                                "5000000000181316459",
                                "5000000000179724207",
                                "5000000000186890241",
                                "5000000000179646168",
                                "5000000000167014179",
                                "5000000000182799268001",
                                "5000000000167003717",
                                "5000000000171684937",
                                "5000000000189194479",
                                "5025800010000008290",
                                "5040100010000002273",
                                "5000000000163511974",
                                "5000000000167002198",
                                "5000000000178112613_999",
                                "5000000000188295298",
                                "5000000000167322907",
                                "5000000000187051497",
                                "15000000000167137912",
                                "5000000000186218384",
                                "5000000000179646824",
                                "5000000000166988752",
                                "5000000000193481097",
                                "5000000000187042508",
                                "5000000000167013866",
                                "5000000000186847245",
                                "5000000000184819392",
                                "5040100010000046630",
                                "5000000000167004236",
                                "5000000000188183427",
                                "5000000000167014828",
                                "5000000000163637149",
                                "5000000010000006393",
                                "5000000010000016406",
                                "5000000000176705153",
                                "5000000000167028205",
                                "5000000000166988987",
                                "5000000000167008969",
                                "5000000000188288348",
                                "5000000000179645950",
                                "5000000000179648891",
                                "5000000000174995488",
                                "5000000000178112694",
                                "5000000000166985940",
                                "5000000000167000528",
                                "5025300010000006781",
                                "5000000000167012998",
                                "5000000010000024007",
                                "5000000000167012512",
                                "5000000000178053985_999",
                                "25000000000174995488",
                                "5000000000186945881",
                                "5000000000181315250",
                                "5000000000187075893",
                                "5000000000177520692",
                                "5000000000167250195",
                                "5000000010000027981",
                                "5000000000183670204",
                                "5000000000180766632",
                                "5000000000188206861",
                                "809643488",
                                "5000000000179646904",
                                "5000000000179232377",
                                "5000000000182648309",
                                "5000000000188485829_999",
                                "5000000000179232375",
                                "5000000000166983876",
                                "5000000000179232379",
                                "5000000000188295228_999",
                                "5000000000192339504",
                                "5000000000166983874",
                                "5000000000179232370",
                                "5000000000179232373",
                                "5000000000191948462",
                                "5000000000179232374",
                                "5000000000179232371"
                            ]
                        }
                    ],
                    "deptId": dbName,
                    "userDbId": "5ab8bc835d635a69645b0c07",
                    "depSpectator": False,
                    "deleted": False,
                    "signAllowed": True,
                    "approveAllowed": True,
                    "orgName": "ГУИП",
                    "lastModified": rldd2.ISODate("2019-12-11T12:00:25.407+0000"),
                    "lastModifiedBy": "rldd2",
                    "_class": "operator"
                }
                upd = db['operators'].insert_one(new_user)
                print(f'{upd.inserted_id}, Has been inserted.')
            except TypeError:
                print(dbName, 'Have no oktmo')
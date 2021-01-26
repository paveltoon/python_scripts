from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
names = [
    "name",
    "srguServiceName",
    "srguDepartmentName",
    "srguServicePassportName"
]
data_names = [
    "customClaimNumber",
    "activationDate",

]
result_file = open('nonames.csv', 'w+')

query = {"activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")}, "oktmo": {'$ne': "99999999"}}
projection = {"_id": 1, "customClaimNumber": 1, "activationDate": 1, "service": 1}
claims = db["claims"].find(query, projection).limit(1000)


def form_string_from_dict(diction: dict):
    result_string = ""
    for value in diction.values():
        result_string += value + ';'
    return result_string[:-1] + "\n"


def add_array_to_obj(obj, arr):
    for i in arr:
        obj[i] = ""


for claim in claims:
    isFound = False
    result = {
        "ccn": claim["customClaimNumber"],
    }
    add_array_to_obj(result, names)
    if "service" in claim:
        for name in names:
            if name in claim["service"]:
                result[name] = claim["service"][name]
            else:
                isFound = True
    else:
        continue
    if isFound:
        result_file.write(form_string_from_dict(result))
result_file.close()

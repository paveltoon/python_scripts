import json
import re

res = open('../07-08-2020 20-32-55 836.json', encoding="utf-8")
needValues = [
    "_id",
    "lastName",
    "firstName",
    "middleName",
    "birthDate",
    "gender",
    "relations",
    "addresses.address_type",
    "addresses.fias",
    "addresses.kladr",
    "addresses.address.country",
    "addresses.address.region",
    "addresses.address.city",
    "addresses.address.street_address",
]


def parseValue(val):
    if "." in val:
        arr = re.split(r'\.', val)
        for el in arr:
            checkObj(arr, el)


def checkValues(obj, val):
    if val in obj:
        return f"{obj[val]};"
    else:
        return ';'


def checkObj(obj, val):
    print(re.split(r'\.', val))


tojson = json.load(res)
result = []
result.append(checkValues(tojson[0], "lastName"))
checkObj(tojson[0], "addresses.address.country")
result_string = "".join(result)[:-1]
print(result_string)

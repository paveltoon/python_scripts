from bson import InvalidBSON

from rldd.client import Client
from rldd import config
import datetime
import sys


def get_age(_date):
    ds = _date.split('-')
    birth_date = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.datetime(
        int(ds[0]), int(ds[1]), int(ds[2])) - datetime.timedelta(days=1)) / 365).days
    return birth_date


def from_birth(_date):
    ds = str(_date).split('-')
    if len(ds[0]) != 4:
        raise ValueError(f"{ds[0]} wrong year")
    return ds[0]


result_file = open('ids.csv', 'w+')
count_result = open('counts.csv', 'w+')
f_count = 0
r_count = 0
db = Client(config.PROD).connect()
dps = Client(config.DPS, "dps").connect()
jact = {"_id": 1, "personsInfo": 1, "pguConsultationInfo": 1}
iteration1 = 0
iteration2 = 0

while True:
    try:
        claims = db["claims"].find({
            "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000"),
                               '$lte': Client.ISODate("2020-09-28T21:00:00.000+0000")},
            "customClaimNumber": {'$regex': '^M.*'},
            "personsInfo": {'$exists': True}}, jact, no_cursor_timeout=True).skip(iteration1)
        try:
            for claim in claims:
                iteration1 += 1
                print("first", iteration1)
                claimId = claim["_id"]
                personsInfo = claim["personsInfo"]
                for person in personsInfo:
                    try:
                        birth = from_birth(person["dateOfBirth"])
                        year = int(birth)
                        if year <= 1954:
                            f_count += 1

                        if year <= 1957:
                            result_file.write(f"{claimId}\n")
                    except KeyError as lu:
                        print(f"{claimId} have no key {lu}")
                    except ValueError as v:
                        print(f"{claimId} has wrong value {v}")
            break
        except:
            print("Unexpected error:", sys.exc_info()[0])
            input()
    except InvalidBSON as e:
        print(e)
        iteration1 += 1
result_file.close()
while True:
    try:
        claimsP = db["claims"].find({
            "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000"),
                               '$lte': Client.ISODate("2020-09-28T21:00:00.000+0000")},
            "customClaimNumber": {'$regex': '^P.*'},
            "personsInfo": {'$exists': True}}, jact, no_cursor_timeout=True).skip(iteration2)
        try:
            for claimP in claimsP:
                iteration2 += 1
                print("second", iteration2)
                claimId = claimP["_id"]
                personsInfo = claimP["personsInfo"]
                for person in personsInfo:
                    try:
                        birth = from_birth(person["dateOfBirth"])
                        year = int(birth)
                        if year <= 1957:
                            if "pguConsultationInfo" in claimP:
                                r_count += 1
                    except KeyError as k:
                        print(f"{claimId} have no key {k}")
                    except ValueError as v:
                        print(f"{claimId} has wrong value {v}")
            break
        except:
            print("Unexpected error:", sys.exc_info()[0])
            input()
    except InvalidBSON as e:
        print(e)
        iteration2 += 1

count_result.write(f"{f_count};{r_count}")
count_result.close()

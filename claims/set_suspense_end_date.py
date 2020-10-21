import datetime

from rldd.client import Client
from rldd import config
from datetime import timedelta

errors_file = open("errors.csv", 'w+')
db = Client(config.PROD).connect()
projection = {"_id": 1, "customClaimNumber": 1, "suspenseReason": 1}


def get_calendar(year: int):
    calendar = db["calendars"].find_one({"year": year, "oktmo": ""})
    if calendar:
        return calendar["daysOff"]


def get_day_of_the_year(date):
    return int(date.timetuple().tm_yday)


def get_suspense_end_date(_claim):
    _ccn = _claim["customClaimNumber"]
    try:
        suspenseReason = _claim["suspenseReason"]
        suspenseCreateDate = suspenseReason["createDate"].replace(hour=0, minute=0, second=0, microsecond=0)
        suspenseDays = int(suspenseReason["suspenseDays"])
        _endDate = suspenseCreateDate + timedelta(days=suspenseDays + 1)
        return _endDate
    except KeyError as _k:
        raise KeyError(_k)


def check_holidays(_date):
    _endDay = get_day_of_the_year(_date)
    calendar = get_calendar(_date.year)
    while _endDay in calendar:
        _endDay += 1
    return datetime.datetime(_date.year, 1, 1) + timedelta(days=_endDay - 1) - timedelta(hours=3)


claims = db["claims"].find({"currStatus.statusCode": "70"},
                           projection).skip(194)
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    try:
        sus = get_suspense_end_date(claim)
        endDate = check_holidays(sus)
        upd = db['claims'].update_one({"_id": claimId}, {"$set": {"suspenseEndDate": endDate}})
        print(
            f"Claim {ccn}, with id: {claimId} has been updated. suspenseEndDate: {endDate}. progress: {upd.modified_count} / {upd.matched_count}.")
    except KeyError as k:
        print(f"Claim {ccn} have no key {k}")
        continue
    except TypeError as t_e:
        errors_file.write(f"{ccn}\n")
        continue

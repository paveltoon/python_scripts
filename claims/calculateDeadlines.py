import pymongo
from bson import ObjectId

from rldd.client import Client
from rldd import config
import datetime


def getAttribute(obj, attr):
    if attr in obj:
        return obj[attr]
    else:
        raise KeyError(f'No attribute {attr} in claim {obj["_id"]}')


def form_deadline_stages(obj):
    if "deadline" in obj and "deadlineInWorkDays" in obj:
        stages = [{
            "stageType": "REGULATION_TIME",
            "stageName": "Регламентный срок",
            "deadline": obj["deadline"],
            "deadlineInWorkDays": obj["deadlineInWorkDays"]
        }]
        if obj["activationDate"].hour >= 16:
            stages.append({
                "stageType": "DEADLINE_TRANSFER",
                "stageName": "Перенос регламентного срока из-за подачи заявки после 16:00",
                "deadline": 1,
                "deadlineInWorkDays": True
            })
        return stages
    else:
        raise KeyError(f'Cant set deadlineStages to claim {obj["_id"]}')


def get_deadline_stages(obj):
    if "deadlineStages" not in obj:
        return form_deadline_stages(obj)
    elif len(obj["deadlineStages"]) == 0:
        return form_deadline_stages(obj)
    else:
        return None


def get_calendar(year: int, claim_id):
    calendar = db["calendars"].find_one({"year": year, "oktmo": ""})
    if calendar is not None:
        return calendar["daysOff"]
    else:
        raise ValueError(f'Can\'t get calendar for {year} year in claim {claim_id}')


def get_day_of_the_year(date):
    return date.timetuple().tm_yday


def calc_workdays(date_from, work_days, days_to_deadline, claim_id):
    calendar = get_calendar(date_from.year, claim_id)
    doy = get_day_of_the_year(date_from)
    ddays = 0 + days_to_deadline
    while work_days > 0:
        if doy in calendar:
            doy += 1
            ddays += 1
        else:
            doy += 1
            work_days -= 1
            ddays += 1

            # Если дедлайн выпадает на новый год
        if doy > get_day_of_the_year(datetime.datetime(date_from.year, 12, 31)):
            calendar = get_calendar(date_from.year + 1, claim_id)
            doy = 1
    deadline_date = date_from.replace(hour=21, minute=0, second=0, microsecond=0) + datetime.timedelta(
        days=ddays) if days_to_deadline == 0 else date_from.replace(hour=21, minute=0, second=0,
                                                                    microsecond=0) + datetime.timedelta(
        days=ddays - days_to_deadline)
    return {
        'daysToDeadline': ddays,
        'deadlineDate': deadline_date,
        'calendar': calendar
    }


def calculate_raw_deadline(full_claim, stages):
    workDays = 0
    calDays = 0
    for st in stages:
        if st["deadlineInWorkDays"]:
            workDays += int(st["deadline"])
        else:
            calDays += int(st["deadline"])

    deadline_data = calc_workdays(full_claim["activationDate"], workDays, 0, full_claim["_id"])

    days_to_deadline = deadline_data["daysToDeadline"] + calDays
    new_deadline_date = deadline_data["deadlineDate"] + datetime.timedelta(days=calDays)

    # Если последний день выпадает на выходной
    if get_day_of_the_year(new_deadline_date) in deadline_data["calendar"]:
        deadline_data = calc_workdays(deadline_data["deadlineDate"] + datetime.timedelta(days=calDays), 1,
                                      days_to_deadline, full_claim["_id"])
        days_to_deadline = deadline_data["daysToDeadline"]
        new_deadline_date = deadline_data["deadlineDate"]
        new_deadline_date -= datetime.timedelta(days=1)

    new_deadline_date -= datetime.timedelta(days=1)
    return {"daysToDeadline": days_to_deadline, "deadlineDate": new_deadline_date}


def checkSuspenseDays(_claim):
    _suspense_days = claim["suspenseReason"]["suspenseDays"]
    _suspense_date = claim["suspenseReason"]["createDate"]

    _result_suspense_date = _suspense_date + datetime.timedelta(days=_suspense_days)
    _result_suspense_days = (_result_suspense_date - datetime.datetime.now()).days + 1
    if _result_suspense_days < 0:
        raise ValueError(f'Claim {claim["customClaimNumber"]} suspenseDays < 0')
    else:
        return _result_suspense_days


def get_statuses(claim_id):
    statuses_list = list(
        db["claims_status"].find({"claimId": str(claim_id), "statusCode": {"$in": ["70", "71"]}}).sort("statusDate",
                                                                                                       pymongo.ASCENDING))
    return statuses_list


projection = {
    "_id": 1,
    "oktmo": 1,
    "claimCreate": 1,
    "activationDate": 1,
    "deadline": 1,
    "deadlineDate": 1,
    "daysToDeadline": 1,
    "deadlineInWorkDays": 1,
    "deadlineStages": 1,
    "customClaimNumber": 1,
    "currStatus": 1,
    "statuses": 1
}

db = Client(config.DEV).connect()
# claims = db["claims"].find({"activationDate": {'$gte': Client.ISODate("2020-01-05T14:33:09.150+0000")}},
#                            projection).skip(100).limit(100)
# claims = db["claims"].find({"_id": {"$in": [ObjectId("5f353a8becbf2800011d24d0")]}})

# claims = db["claims"].find({"deadlineDate": {'$gte': Client.ISODate("2021-01-01T21:00:00.000+0000")}})

# SuspenseDays query
claims = db["claims"].find({
    "activationDate": {'$gte': Client.ISODate("2019-06-01T00:00:00.000+0000")},
    "suspenseDays": {'$exists': True},
    "daysToDeadline": {'$gt': 0}
})

for claim in claims:
    try:
        updater = {}
        claimId = claim["_id"]
        activationDate = getAttribute(claim, "activationDate")
        deadlineStages = get_deadline_stages(claim)
        if deadlineStages is not None:
            updater["deadlineStages"] = deadlineStages
        else:
            deadlineStages = claim["deadlineStages"]

    except KeyError as k:
        print(k)
        continue
    except ValueError as v:
        print(v)
        continue

    deadlines = calculate_raw_deadline(claim, deadlineStages)
    raw_daysToDeadline = deadlines["daysToDeadline"]
    deadlineDate = deadlines["deadlineDate"]
    daysToDeadline = int

    end_point = claim["docSendDate"] if "docSendDate" in claim else datetime.datetime.now()

    daysToDeadline = (deadlineDate - end_point).days + 1

    if "suspenseDays" in claim:
        suspenseReason = claim["suspenseReason"]
        suspenseDays = suspenseReason["suspenseDays"]
        suspenseWorkdays = suspenseReason["workingDays"]
        suspenseDate = suspenseReason["createDate"]

         # Прогон по статусам
        statuses = get_statuses(claimId)
        dif_days = 0
        for i in range(len(statuses) - 1):
            if statuses[i + 1]["statusCode"] == "71":
                status = statuses[i]
                status_code = status["statusCode"]
                status_date = status["statusDate"]
                dif_days += (statuses[i + 1]["statusDate"] - status_date).days

        # Добавляем дни между статусами к дедлайну
        deadlineDate += datetime.timedelta(days=dif_days)
        daysToDeadline = (deadlineDate - end_point).days + 1
        # Проверка на существующий 70 статус.
        if claim["currStatus"]["statusCode"] == "70":
            current_suspense_days = claim["suspenseReason"]["suspenseDays"]
            deadlineDate += datetime.timedelta(days=current_suspense_days)

            suspense_days_claim = checkSuspenseDays(claim)
            updater["suspenseDays"] = suspense_days_claim
    updater["deadlineDate"] = deadlineDate
    updater["daysToDeadline"] = daysToDeadline
    print(claimId, daysToDeadline, deadlineDate, updater)

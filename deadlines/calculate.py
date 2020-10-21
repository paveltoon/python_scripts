from time import sleep
import pymongo
from bson import InvalidBSON
from rldd.client import Client
from rldd import config
import datetime
import requests
from colors import console_colors

yellow = console_colors.CYELLOW
end = console_colors.CEND

db = Client(config.PROD).connect()
processed = 0
insert_count = 0

# query = {
#     "activationDate": {'$gte': Client.ISODate("2019-12-31T21:00:00.000+0000")},
#     "senderCode": {'$ne': "MBKT"},
#     "resultStatus": {'$exists': False}
# }

query = {"customClaimNumber": "P001-7900168090-23268829"}

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
    "statuses": 1,
    "suspenseReason": 1,
    "suspenseDays": 1
}


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
    if calendar:
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


def send_to_claim_deadline_changes(_claim_id, _previous_deadline_date, _next_deadline_date):
    __document = {
        "createDate": datetime.datetime.now() - datetime.timedelta(hours=3),
        "previousDeadlineDate": _previous_deadline_date,
        "nextDeadlineDate": _next_deadline_date,
        "claimId": _claim_id
    }

    _upd = db["claim_deadline_changes"].insert_one(__document)

    if _upd.inserted_id:
        global insert_count
        insert_count += 1
        print(insert_count)
        if insert_count >= 100:
            while check_deadline_changes_queue().json()["totalCount"] != 0:
                sleep(1)  # Стучимся каждую секунду в АПИ для проверки, что все заявки отправились


def check_deadline_changes_queue():
    res = requests.get("http://10.10.80.54:8080/api/troubleshooting/claim-deadline-changes/notify")
    return res


def calculate_suspense_days(suspense_reason, curr_status, _deadline_date, _end_point):
    suspenseDays = suspense_reason["suspenseDays"]

    # Прогон по статусам
    statuses = get_statuses(claimId)
    dif_days = 0
    for i in range(len(statuses) - 1):
        if statuses[i + 1]["statusCode"] == "71":
            status = statuses[i]
            status_date = status["statusDate"]
            dif_days += (statuses[i + 1]["statusDate"] - status_date).days

    # Добавляем дни между статусами к дедлайну
    _deadline_date += datetime.timedelta(days=dif_days)
    _daysToDeadline = (_deadline_date - _end_point).days + 1
    # Проверка на существующий 70 статус.
    if curr_status["statusCode"] == "70":
        _deadline_date += datetime.timedelta(days=suspenseDays)
        suspense_days_claim = checkSuspenseDays(claim)
        updater["suspenseDays"] = suspense_days_claim
        _daysToDeadline += suspenseDays - suspense_days_claim  # Имитация приостановки дедлайна

    return {
        "deadlineDate": _deadline_date,
        "daysToDeadline": _daysToDeadline
    }


while True:
    try:
        claims = db["claims"].find(query, projection, no_cursor_timeout=True).skip(processed).limit(2000)
        for claim in claims:
            try:
                processed += 1
                updater = {}
                claimId = claim["_id"]
                ccn = claim["customClaimNumber"]
                origDeadlineDate = claim["deadlineDate"]
                activationDate = getAttribute(claim, "activationDate")

                deadlineStages = get_deadline_stages(claim)
                if deadlineStages is not None:
                    updater["deadlineStages"] = deadlineStages
                else:
                    deadlineStages = claim["deadlineStages"]

                deadlines = calculate_raw_deadline(claim, deadlineStages)
                end_point = claim["docSendDate"] if "docSendDate" in claim else datetime.datetime.now()

                raw_daysToDeadline = deadlines["daysToDeadline"]
                deadlineDate = deadlines["deadlineDate"]
                daysToDeadline = (deadlineDate - end_point).days + 1

                if "suspenseReason" in claim:
                    sus = calculate_suspense_days(claim["suspenseReason"], claim["currStatus"], deadlineDate, end_point)
                    deadlineDate = sus["deadlineDate"]
                    daysToDeadline = sus["daysToDeadline"]

                updater["deadlineDate"] = deadlineDate
                updater["daysToDeadline"] = daysToDeadline
                upd = db["claims"].update_one({"_id": claimId}, {"$set": updater})

                if origDeadlineDate != deadlineDate:
                    send_to_claim_deadline_changes(str(claimId), origDeadlineDate, deadlineDate)

            except KeyError as k:
                print(k)
                continue
            except ValueError as v:
                print(v)
                continue

            print(processed, yellow + ccn + end, claimId, daysToDeadline, deadlineDate, f"{upd.modified_count} / {upd.matched_count}")
        check_deadline_changes_queue()
        break
    except InvalidBSON as e:
        print(e)
        processed += 1

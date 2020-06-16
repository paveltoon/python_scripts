from rldd import rldd2
from user import rldd_user
import bson
from datetime import datetime, timedelta

log = open('add_deadlines_covid.log', 'w+')
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
# db = rldd2.LOCAL_connect('local')
total = 0
corrected = 0
claims = db["claims"].find({"$or": [{"deadlineInWorkDays": False}, {"deadlineStages.deadlineInWorkDays": False}],
                            "resultStatus": {"$exists": False},
                            "activationDate": {"$gte": rldd2.ISODate("2019-07-31T21:00:00.000+0000")}})
# claims = db["claims"].find({"$or": [{"deadlineInWorkDays": False}, {"deadlineStages.deadlineInWorkDays": False}],
#                             "resultStatus": {"$exists": False},
#                             "activationDate": {"$gte": rldd2.ISODate("2020-03-10T21:00:00.000+0000"),
#                                                "$lte": rldd2.ISODate("2020-03-20T21:00:00.000+0000")}})
for claim in claims:
    total += 1
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    full_deadline = 0
    isWorkingDays = False
    total_days_to_deadline = 0
    print(ccn)
    try:
        if claim["deadlineInWorkDays"] is True:
            continue
        # Проверка дедлайна в стейджах
        if 'deadlineStages' in claim:
            if len(claim['deadlineStages']):
                for stage in claim['deadlineStages']:
                    if 'stageType' in stage:
                        if stage['stageType'] == "REGULATION_TIME" and stage['deadlineInWorkDays'] is True:
                            isWorkingDays = True
                    full_deadline += stage['deadline']
        else:
            full_deadline = claim["deadline"]

        if isWorkingDays is True:
            continue
        # Проверка даты активации заявки
        if 'activationDate' in claim:
            activation_date = datetime.date(claim['activationDate'])
            COVID_day = datetime(2020, 3, 30).date()
            diff_days = (COVID_day - activation_date).days
            if diff_days <= 0:
                total_days_to_deadline = full_deadline
            else:
                total_days_to_deadline = full_deadline - diff_days
            if total_days_to_deadline < 0:
                print(f'[WARNING] {ccn}, deadline < 0 ({total_days_to_deadline}), skipped.')
                log.write(f'[WARNING] {ccn}, deadline < 0 ({total_days_to_deadline}), skipped.\n')
                continue
            total_deadline_date = str(datetime.date(claim['deadlineDate']) + timedelta(days=total_days_to_deadline))
            fd = total_deadline_date.split('-')
            new_deadline_date = datetime(int(fd[0]), int(fd[1]), int(fd[2])) - timedelta(hours=3)
            new_days_to_deadline = total_days_to_deadline + int(claim["daysToDeadline"])
            upd = db["claims"].update_one({"_id": claimId}, {
                "$set": {
                    "deadlineDate": new_deadline_date,
                    "daysToDeadline": new_days_to_deadline
                }
            })
            update_print = f'Claim: {ccn} has been correcter. progress: {upd.modified_count} / {upd.matched_count}'
            print(update_print)
            log.write(f'{update_print}\n')
            corrected += upd.modified_count
    except KeyError:
        print(f'KeyError in {claim["customClaimNumber"]}')
        continue
    except bson.errors.InvalidBSON:
        print(f'Error in {claim["customClaimNumber"]}')
        continue
    except:
        print(f'Error in {claim["customClaimNumber"]}')
        continue
log.close()
print(f'Всего заявок найдено: {total}\nЗаявок обработано: {corrected}')

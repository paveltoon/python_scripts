from rldd import rldd2
from user import rldd_user
import re
import bson

result_file = open('regex.txt', 'w+', encoding='utf-8')


# Functions
def regex0(regex):
    return re.findall(Regexps[0]['regex'], regex)[0]


def regex1(regex):
    form = re.findall(Regexps[1]['regex'], regex)[0]
    n = form.split('-')
    months = {
        'янв': '01',
        'фев': '02',
        'мар': '03',
        'апр': '04',
        'май': '05',
        'мая': '05',
        'июн': '06',
        'июл': '07',
        'авг': '08',
        'сен': '09',
        'окт': '10',
        'ноя': '11',
        'дек': '12'
    }
    return str(f'{n[2]}-{months[n[1]]}-{n[0]}')


# Global variables
Regexps = [
    {
        'regex': r'\d{4}-\d\d-\d\d',
        'function': regex0,
    },
    {
        'regex': r'\d\d-\D{3}-\d{4}',
        'function': regex1,
    },
]

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
persons = db['persons'].find({"dateOfBirth": {'$exists': True}})
for person in persons:
    _id = person['_id']
    dateOfBirth = str(person['dateOfBirth']).strip()
    if str(dateOfBirth).strip() == '':
        continue
    isMatched = False
    formatted_date_of_birth = str
    update_data = {}
    try:
        if 'currIdentityDoc' in person:
            if 'fromDate' in person['currIdentityDoc']:
                fromDate = person['currIdentityDoc']['fromDate']
                for reg in Regexps:
                    if re.search(reg['regex'], fromDate):
                        isMatched = True
                        update_data['currIdentityDoc.fromDate'] = reg['function'](fromDate)
        for reg in Regexps:
            if re.search(reg['regex'], dateOfBirth):
                isMatched = True
                update_data['dateOfBirth'] = reg['function'](dateOfBirth)
        if not isMatched:
            result_file.write(f'{dateOfBirth}\n')
            print(f'[WARNING] No Regex with {dateOfBirth} value.')
            continue
        if len(update_data['dateOfBirth']) != 10:
            result_file.write(f'{update_data["dateOfBirth"]}\n')
            continue
        # UPDATE
        upd = db['persons'].update_one({"_id": _id}, {"$set": update_data})
        print(f'{_id} was corrected. progress: {upd.modified_count} / {upd.matched_count}')
    except Exception as err:
        print(_id, err)
result_file.close()

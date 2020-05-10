from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
upd1 = db['claims'].update_many(
    {"service.srguDepartmentId": "5000000010000000315", "service.srguServicePassportId": "5000000010000033577",
     "service.srguDepartmentName": {'$exists': False}}, {
        '$set': {
            'service.srguDepartmentName': 'Министерство сельского хозяйства и продовольствия Московской области'
        }
    })
print(f'{upd1.modified_count} / {upd1.matched_count}')

upd2 = db['claims'].update_many(
    {"service.srguDepartmentId": "5000000010000000315", "service.srguServicePassportId": "5000000010000033577",
     "service.srguDepartmentName": {'$exists': False}, "service.srguServicePassportName": {'$exists': False},
     "oktmo": {'$ne': "99999999"}}, {
        '$set': {
            "service.srguDepartmentName": "Министерство сельского хозяйства и продовольствия Московской области",
            "service.srguServicePassportName": "Выдача и аннулирование охотничьих билетов",
        }
    })
print(f'{upd2.modified_count} / {upd2.matched_count}')

upd3 = db['claims'].update_many(
    {"service.srguDepartmentId": "5000000010000000315", "service.srguServicePassportId": "5000000010000033577",
     "service.srguServicePassportName": {'$exists': False}, "oktmo": {'$ne': "99999999"}}, {
        '$set': {
            "service.srguDepartmentName": "Министерство сельского хозяйства и продовольствия Московской области",
            "service.srguServicePassportName": "Выдача и аннулирование охотничьих билетов",
        }
    })
print(f'{upd3.modified_count} / {upd3.matched_count}')

upd4 = db['claims'].update_many(
    {"service.srguDepartmentId": "5000000010000000315", "service.srguServicePassportId": "5000000010000033577",
     "provLevel": {'$exists': False}, "oktmo": {'$ne': "99999999"}}, {
        '$set': {
            "provLevel": "Региональный"
        }
    })
print(f'{upd4.modified_count} / {upd4.matched_count}')
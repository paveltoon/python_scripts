import os.path
import pandas as pd
from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
homedir = os.path.expanduser('~')
file = pd.read_csv(f'{homedir}\\Desktop\\legalForm.csv')
# file = pd.read_csv('legalForm.csv', encoding='utf-8')
for index, row in file.iterrows():
    this_row = row.values[0].split(";")
    _id = rldd2.getId(this_row[0])
    legalForm = this_row[1]
    person = db["persons"].find_one({"_id": _id})
    if person is not None:
        upd = db["persons"].update_one({"_id": _id}, {"$set": {"legalForm": legalForm}})
        print(f'{_id} {upd.modified_count} / {upd.matched_count}')
    else:
        print(f'{_id} Не найден в РЛДД')
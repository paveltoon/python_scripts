import pandas as pd
from rldd import rldd2
from user import rldd_user
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
file = pd.read_csv('parts/snils4.csv', dtype=str)

counter = {
    "phones": 0,
    "emails": 0,
    "emails&phones": 0,
    "totalResult": 0
}

for index, snilsCSV in file.iterrows():
    if index % 1000 == 0:
        print(index)
    person = db["persons"].find_one({"snils": snilsCSV["snils"]})
    if person is None:
        formatSnils = f'{snilsCSV["snils"][:3]}-{snilsCSV["snils"][3:6]}-{snilsCSV["snils"][6:9]}' \
                      f' {snilsCSV["snils"][9:]}'
        person = db["persons"].find_one({"snils": formatSnils})
        if person is None:
            file.loc[index, 'isFound'] = 'False'
        continue

    contacts = {
        "phone": [],
        "email": [],
    }

    hasPhone = False
    hasEmail = False
    counter["totalResult"] += 1
    try:
        if person["contacts"] is not None and len(person["contacts"]):
            for contact in person["contacts"]:
                if contact["type"] == 'EML':
                    contacts["email"].append(contact["value"])
                    counter["emails"] += 1
                    hasEmail = True
                else:
                    contacts["phone"].append(contact["value"])
                    counter["phones"] += 1
                    hasPhone = True

        if hasPhone and hasEmail:
            counter["emails&phones"] += 1
        file.loc[index, 'phone'] = ",".join(contacts["phone"])
        file.loc[index, 'email'] = ",".join(contacts["email"])
    except KeyError:
        file.loc[index, 'error'] = "contacts not found"
        print(index, snilsCSV["snils"], 'has error!')
    except Exception:
        file.loc[index, 'error'] = "other errors"
file.to_csv('statistic4.csv', sep=';', encoding='utf-8-sig', index=False)
print(counter)

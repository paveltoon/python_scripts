import datetime

from rldd.client import Client
from rldd import config

db = Client(config.DPS, "dps").connect()
result_file = open("persons.csv", "w+")
result_file.write("Фамилия;Имя;Отчество;Есиа Айди;Снилс;Email;Телефон\n")


def get_fio(_obj):
    _result = ""
    if "surname" in _obj:
        if _obj["surname"].strip() != "":
            _result += _obj["surname"]
    if "firstName" in _obj:
        if _obj["firstName"].strip() != "":
            _result += _obj["firstName"]
    if "middleName" in _obj:
        if _obj["middleName"].strip() != "":
            _result += _obj["middleName"]
    return _result.strip()


def get_age(_date):
    ds = _date.split('-')
    birth_date = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.datetime(
        int(ds[0]), int(ds[1]), int(ds[2])) - datetime.timedelta(days=1)) / 365).days
    return birth_date


def getContact(obj, con_type):
    con_list = []
    if "contacts" in obj:
        contacts = obj["contacts"]
        if len(contacts) > 0:
            for c in contacts:
                if "type" in c:
                    if c["type"] == con_type:
                        con_list.append(c["value"])
            return ", ".join(con_list)
        else:
            return ''
    return ''


query = {"type": "PHYSICAL", "technicalProperties.type": "GOLD", "esiaAutorisation": True}
projection = {"contacts": 1, "surname": 1, "firstName": 1, "middleName": 1, "dateOfBirth": 1, "snils": 1,
              "esiaAutorisation": 1, "esiaId": 1, "esia": 1}

persons = db["persons"].find(query, projection)
for person in persons:
    try:
        age = get_age(person["dateOfBirth"])
        if age >= 16:
            result = {
                "surname": person["surname"] if "surname" in person else "",
                "firstName": person["firstName"] if "firstName" in person else "",
                "middleName": person["middleName"] if "middleName" in person else "",
                "esiaId": "",
                "snils": person["snils"] if "snils" in person else "",
                "dateOfBirth": person["dateOfBirth"] if "dateOfBirth" in person else "",
                "email": getContact(person, "EML").strip(),
                "phone": getContact(person, "PHN").strip(),
            }
            result["phone"] += " " + getContact(person, "MBT") if getContact(person, "MBT") != "" else ""

            if "esiaId" in person:
                result["esiaId"] = person["esiaId"]
            elif "esia" in person:
                result["esiaId"] = person["esia"]["id"]
            result_string = ""
            for value in result.values():
                result_string += value + ";"
            result_file.write(result_string[:-1] + "\n")
            print(result_string)
    except KeyError as k:
        print("[ERROR]", k, "no key", person["_id"])
        continue
    except ValueError as v:
        print("[ERROR]", v, "value error", person["_id"])

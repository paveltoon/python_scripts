import csv

from rldd.client import Client
from rldd import config

pers = Client(config.DPS, "dps").connect()
adr = Client(config.PROD).connect()

result_file = open('statistic.csv', 'w+', encoding='utf-8')
iteration = 0


def getAddress(_id):
    _address = adr["addresses"].find_one({"_id": Client.getId(_id)})
    if "_class" in _address:
        del _address["_class"]
    return _address


def checkValue(obj, val):
    if val in obj:
        return f"{obj[val]}"
    else:
        return ''


def getFio(_person):
    return f'{checkValue(_person, "surname")} {checkValue(_person, "firstName")} {checkValue(_person, "middleName")}'


def get_contact(doc, *contact_types):
    contact_list = []
    if "contacts" in doc:
        isFound = False
        for contact_type in contact_types:
            for cont in doc["contacts"]:
                if "type" in cont:
                    if cont["type"] == contact_type:
                        if "value" in cont:
                            contact_list.append(cont["value"])
                            isFound = True
        if isFound:
            return ", ".join(contact_list)
        else:
            return ''
    else:
        return ''


fields = [
    'ОМСУ',
    'Населенный пункт',
    'Улица',
    'Номер дома',
    'Квартира',
    'ФИО',
    'Телефон',
    'Электронная почта'
]
projection = {"surname": 1, "firstName": 1, "middleName": 1, "contacts": 1, "registrationAddressId": 1}
result_file.write(';'.join(fields) + '\n')

with open('data.txt') as data:
    # Convert CSV to LIST, set start position
    lines = list(csv.reader(data, delimiter="\n"))[2811971:]
    for row in lines:

        person = pers["persons"].find_one({"_id": Client.getId(row[0])}, projection)
        if person:
            iteration += 1
            address = getAddress(checkValue(person, 'registrationAddressId')) if checkValue(person,
                                                                                            'registrationAddressId') != '' else ''
            result = {
                'omsu': checkValue(address, "area"),
                'locality': checkValue(address, "locality"),
                'street': checkValue(address, "street"),
                'houseNumber': checkValue(address, "houseNumber"),
                'room': checkValue(address, "room"),
                'fio': getFio(person),
                "phone": get_contact(person, "MBT", "PHN"),
                "email": get_contact(person, "EML")
            }
            res_string = ''
            for res in result.values():
                res_string += res + ';'
            result_file.write(res_string[:-1] + '\n')
            print(iteration)
result_file.close()

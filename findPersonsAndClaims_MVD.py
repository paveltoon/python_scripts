from rldd.client import Client
from rldd import config

persons = Client(config.DPS, "dps").connect()["persons"]
prod = Client(config.PROD).connect()

persons_list = [
    "57b3284ca78e509d2b6357ec",
    "565fd4cba78e53d22a97d918",
    "58dbced9a78e25942a1dfad5",
    "5e00d9b322e5c60001fb531b",
    "5e00d9b322e5c60001fb5300",
    "5e17735722e5c60001f0e53d",
    "5e17735722e5c60001f0e572",
    "5ab8e8f3a78e0d1980e09168",
    "5ab8e8f0a78edc558c34be7f",
    "5ab8e8f3a78e0d1980e0918a",
    "5af1582da78e7efb1d2d6adf",
    "5af40cb3a78e97f0e7501e2a",
    "5af40cb6a78ed46ec894fcb0",
    "5af40cb7a78e97f0e7501e92",
    "5af40cb8a78e97f0e7501eb3",
    "5af40cb8a78e97f0e7501edc",
    "5af41d05a78e97f0e7517695",
    "5af41d0ca78e97f0e7517739",
    "5af40f91a78ed46ec8953ba9",
    "5af409a8a78ed46ec894baa2",
    "5c07d6a44cb2f97ddcb30e05"
]


def get_claims_from_person_id(_db, _person_id):
    claims_list = []
    _claims = prod[_db].find({"persons": str(_person_id)})
    for _claim in _claims:
        claims_list.append({
            "ccn": _claim["customClaimNumber"] or None,
            "serviceName": _claim["service"]["name"] or None,
            "activationDate": _claim["activationDate"].isoformat() or None
        })
    return claims_list


def getAddress(_id):
    _address = prod["addresses"].find_one({"_id": Client.getId(_id)})
    if "_class" in _address:
        del _address["_class"]
    if _address:
        return _address
    return ''


def checkValue(obj, val):
    if val in obj:
        return f"{obj[val]}"
    else:
        return ''


def getFio(_person):
    return f'{checkValue(_person, "surname")} {checkValue(_person, "firstName")} {checkValue(_person, "middleName")}'


def form_address(_address):
    _arr = [
        checkValue(_address, "region"),
        checkValue(_address, "street"),
        checkValue(_address, "houseNumber"),
        checkValue(_address, "room")
    ]
    new_arr = list(filter(lambda item: item.strip() != "", _arr))

    return ", ".join(new_arr)


def get_contact(_doc, *contact_types):
    contact_list = []
    if "contacts" in _doc:
        _isFound = False
        for contact_type in contact_types:
            for cont in _doc["contacts"]:
                if "type" in cont:
                    if cont["type"] == contact_type:
                        if "value" in cont:
                            contact_list.append(cont["value"])
                            _isFound = True
        if _isFound:
            return ", ".join(contact_list)
        else:
            return ''
    else:
        return ''


fields = [
    'ФИО',
    'Телефоны',
    'Почта',
    'Дата рождения',
    'ДУЛ Серия',
    'ДУЛ Номер',
    'Адрес регистрации',
    'Адрес проживания',
    'Номера заявок',
    'Дата создания заявления',
    'Наименование процедуры'
    'Номера автомобиля'
]

result_file = open('result_file.csv', 'w+')
result_file.write(f'{";".join(fields)}\n')
for person_id in persons_list:

    person = persons.find_one({"_id": Client.getId(person_id)})

    if not person:
        continue

    reg_address = getAddress(checkValue(person, 'registrationAddressId')) if checkValue(person,
                                                                                        'registrationAddressId') != '' else ''
    loc_address = getAddress(checkValue(person, 'locationAddressId')) if checkValue(person,
                                                                                    'locationAddressId') != '' else ''

    result = {
        'fio': getFio(person),
        "phone": get_contact(person, "MBT", "PHN"),
        "email": get_contact(person, "EML"),
        "birth": checkValue(person, "dateOfBirth"),
        "serial": "",
        "number": "",
        'reg_address': form_address(reg_address),
        'loc_address': form_address(loc_address),
        'ccn': [],
        'createDate': [],
        'serviceNames': [],
        'autoNum': ''
    }

    claims_from_all_years = [
        get_claims_from_person_id("claims", person_id),
        get_claims_from_person_id("claims_2015", person_id),
        get_claims_from_person_id("claims_2016", person_id),
        get_claims_from_person_id("claims_2017", person_id),
        get_claims_from_person_id("claims_2018", person_id)
    ]

    for claims in claims_from_all_years:
        for claim in claims:
            result['ccn'].append(claim['ccn'])
            result['createDate'].append(claim['activationDate'])
            result['serviceNames'].append(claim['serviceName'])

    if "identityDocuments" in person:
        docs = person["identityDocuments"]
        for doc in docs:
            if doc["actual"]:
                try:
                    result["serial"] = doc["serial"]
                    result["number"] = doc["number"]
                except KeyError:
                    continue
    if result["number"]:
        ccns = prod["claims"].find(
            {"service.srguServicePassportId": "5000000000215655779", "permitFields.type": "DOC_NUMBER",
             "permitFields.value": result["number"]})
        for claim in ccns:
            ccn = claim["customClaimNumber"]
            if "permitFields" in claim:
                isFound = False
                for permit in claim["permitFields"]:
                    if permit["type"] == "DOC_SERIAL" and permit["value"] == result["serial"]:
                        result['ccn'].append(ccn)
                        isFound = True
                    if permit["type"] == "VEHICLE_NUMBER" and isFound:
                        result['autoNum'] = permit["value"]
        result['ccn'] = ", ".join(result['ccn'])
        result['createDate'] = ", ".join(result['createDate'])
        result['serviceNames'] = ", ".join(result['serviceNames'])
    result_string = ''
    for value in result.values():
        if value is None:
            result_string += ';'
        if isinstance(value, list):
            result_string += ", ".join(value) + ';'
        else:
            result_string += value + ';'
    result_file.write(f"{result_string[:-1]}\n")
result_file.close()

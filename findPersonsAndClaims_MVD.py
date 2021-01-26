from rldd.client import Client
from rldd import config

persons = Client(config.DPS, "dps").connect()["persons"]
prod = Client(config.PROD).connect()

persons_list = [
    "5c126b739f52196d8a246cc4"
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
                result["serial"] = doc["serial"]
                result["number"] = doc["number"]
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

import re

from pymongo.errors import DuplicateKeyError

from rldd.client import Client
from rldd import config
from datetime import datetime

from bson import ObjectId

dps = Client(config.DPS, "dps").connect()
rldd = Client(config.PROD, "rldd2").connect()

regions = {
    "Балаш": "117",
    "Мытищ": "117",
    "Реутов": "117",

    "Долгопр": "118",
    "Дубн": "118",
    "Лобн": "118",
    "Талдом": "118",
    "Дмитр": "118",
    "Лунев": "118",
    "Химк": "118",

    "Колом": "119",
    "Воскресен": "119",
    "Егорьевск": "119",
    "Зарайск": "119",
    "Луховиц": "119",
    "Серебрян": "119",

    "Восход": "120",
    "Волоколамск": "120",
    "Истринск": "120",
    "Клинск": "120",
    "Красногорск": "120",
    "Лотошин": "120",
    "Андреев": "120",
    "Кривцов": "120",
    "Кутузов": "120",
    "Менделеев": "120",
    "Пешковск": "120",
    "Поваров": "120",
    "Ржавк": "120",
    "Смирновск": "120",
    "Соколовск": "120",
    "Солнечногорск": "120",
    "Шаховск": "120",

    "Бронниц": "121",
    "Дзержинск": "121",
    "Жуковск": "121",
    "Котельн": "121",
    "Любер": "121",
    "Раменс": "121",

    "Власих": "122",
    "Звенигород": "122",
    "Краснознаменск": "122",
    "Молодеж": "122",
    "Можайск": "122",
    "Наро-": "122",
    "Одинцов": "122",
    "Руз": "122",

    "Орехово-": "123",
    "Рошал": "123",
    "Электрогорск": "123",
    "Электростал": "123",
    "Павлово-": "123",
    "Шатур": "123",

    "Домодедов": "124",
    "Лыткар": "124",
    "Подольск": "124",
    "Ленин": "124",

    "Королев": "125",
    "Красноармейск": "125",
    "Пушкин": "125",
    "Сергиев": "125",

    "Кашир": "126",
    "Озер": "126",
    "Протвин": "126",
    "Пущин": "126",
    "Серпухов": "126",
    "Ступ": "126",
    "Чехов": "126",

    "Звезд": "127",
    "Ивантеев": "127",
    "Лосино": "127",
    "Фрязин": "127",
    "Черноголов": "127",
    "Ногинск": "127",
    "Щелков": "127",
}


def get_attribute(doc, field):
    if field in doc:
        return doc[field]
    else:
        return ''


def get_prefix(doc, field):
    if get_attribute(doc, field) != '':
        if f"{field}Prefix" in doc:
            if doc[f"{field}Prefix"].strip() != '':
                return f"{doc[field]} {doc[f'{field}Prefix']}"
    return get_attribute(doc, field)


def get_contact(doc, *contact_types):
    contact_list = []
    if "contacts" in doc:
        isFound = False
        for contact_type in contact_types:
            for cont in doc["contacts"]:
                if "type" in cont:
                    if cont["type"] == contact_type:
                        contact_list.append(cont["value"])
                        isFound = True
        if isFound:
            return ", ".join(contact_list)
        else:
            return ''
    else:
        return ''


def person_has_reject(objId):
    return rldd["claims"].count_documents({"persons": str(objId), "resultStatus": "4"}) > 0


def person_has_claims(objId):
    return rldd["claims"].count_documents({"persons": str(objId)}) > 0


def get_string_address(obj, param):
    AddressId = get_attribute(obj, param)
    if AddressId != '':
        address_projection = {
            "country": 1,
            "region": 1,
            "area": 1,
            "locality": 1,
            "street": 1,
            "houseNumber": 1,
            "corps": 1,
            "room": 1,
            "countryPrefix": 1,
            "regionPrefix": 1,
            "areaPrefix": 1,
            "localityPrefix": 1,
            "streetPrefix": 1,
            "houseNumberPrefix": 1,
            "corpsPrefix": 1,
            "roomPrefix": 1,
        }
        address = rldd["addresses"].find_one({"_id": ObjectId(AddressId)}, address_projection)
        if address is not None:
            addressObj = {
                "country": get_prefix(address, "country"),
                "region": get_prefix(address, "region"),
                "area": get_prefix(address, "area"),
                "locality": get_prefix(address, "locality"),
                "street": get_prefix(address, "street"),
                "houseNumber": f'д. {get_prefix(address, "houseNumber")}' if get_prefix(address,
                                                                                        "houseNumber") != '' else '',
                "corps": get_prefix(address, "corps"),
                "room": f'кв. {get_prefix(address, "room")}' if get_prefix(address, "room") != '' else ''
            }
            reg_adr = []
            for adr in list(addressObj.keys()):
                if addressObj[adr] == '':
                    del addressObj[adr]
                else:
                    reg_adr.append(addressObj[adr])
            return ", ".join(reg_adr)
    return ''


def process_one_person(_person):
    try:
        updater = {
            "_id": _person["_id"],
            "surname": get_attribute(_person, "surname"),
            "firstName": get_attribute(_person, "firstName"),
            "middleName": get_attribute(_person, "middleName"),
            "senderName": "DPS",
            "dateOfBirth": get_attribute(_person, "dateOfBirth"),
            "email": get_contact(_person, "EML"),
            "phone": get_contact(_person, "PHN", "MBT", "CPH"),
            "locationAddress": get_string_address(_person, "locationAddressId").strip(),
            "workAddress": get_string_address(_person, "ipWorkPlaceAddressId").strip(),
            "hasClaims": person_has_claims(_person["_id"]),
            "hasRejects": person_has_reject(_person["_id"]),
            "snils": get_attribute(_person, "snils"),
        }

        for elem in regions:
            result = re.search(elem, updater["locationAddress"])
            if result:
                updater["regionCode"] = regions[result.group(0)]
                break
        isFound = dps["xxx_dps_persons"].find_one({"_id": _person["_id"]})
        if isFound:
            print(f"[SKIPPED] {_person['_id']}")
            return
        inserted = dps["xxx_dps_persons"].insert_one(updater)
        print(f"[ADDED] {inserted.inserted_id}")
    except DuplicateKeyError as exception:
        personId = _person["_id"]
        print(f"[DUPLICATE] {personId} {exception}")


pj = {
    "contacts": 1,
    "surname": 1,
    "firstName": 1,
    "middleName": 1,
    "dateOfBirth": 1,
    "snils": 1,
    "esiaAutorisation": 1,
    "esiaId": 1,
    "esia": 1,
    "locationAddressId": 1,
    "registrationAddressId": 1,
    "ipWorkPlaceAddressId": 1
}
persons_query = {
    "type": "PHYSICAL",
    "technicalProperties.type": "GOLD"
}

# Main body
persons = dps["persons"].find(persons_query, pj, no_cursor_timeout=True).skip(7000000)
start = datetime.now()
for person in persons:
    process_one_person(person)
end = datetime.now()

print(f"{start} - {end}")

input()

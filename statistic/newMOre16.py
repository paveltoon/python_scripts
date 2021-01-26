from bson import InvalidBSON

from rldd.client import Client
from rldd import config
import csv

dps = Client(config.DPS, "dps").connect()
prod = Client(config.PROD).connect()


class ExcelRow:
    def __init__(self, _row):
        self.row = {
            "surname": _row[0],
            "firstName": _row[1],
            "middleName": _row[2],
            "dateOfBirth": _row[3],
            "email": _row[4],
            "phone": _row[5],
            "locationAddress": _row[6],
            "workAddress": _row[7],
            "hasClaims": _row[8],
            "hasRejects": _row[9],
            "socialId": _row[10],
            "snils": _row[11]
        }
        self.format_snils()

    def get_row(self):
        newArr = []
        for val in self.row.values():
            newArr.append(val)
        return newArr

    def format_snils(self):
        newForm = "".join(self.row["snils"].split("-"))
        self.row["snils"] = "".join(newForm.split(" ")).strip()


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
    proj = {
        "_id": 1
    }
    return len(list(prod["claims"].find({"persons": str(objId), "resultStatus": "4"}, proj))) > 0


def person_has_claims(objId):
    proj = {
        "_id": 1
    }
    return len(list(prod["claims"].find({"persons": str(objId)}, proj))) > 0


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
        address = prod["addresses"].find_one({"_id": Client.getId(AddressId)}, address_projection)
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
    "technicalProperties.type": "GOLD",
    "esiaAutorisation": True
}
persons = dps["persons"].find(persons_query, pj)

# Main body

iteration = 0
while True:
    try:
        persons = dps["persons"].find(persons_query, pj).skip(iteration)
        for person in persons:
            iteration += 1
            if "snils" in person:
                same_person = dps["xxx_rpgu_persons"].find_one({"snils": person["snils"]})
                if same_person:
                    # Если есть адрес, то пропустить, если нет, то записать
                    updater = {
                        "workAddress": get_string_address(person, "ipWorkPlaceAddressId"),
                        "hasClaims": person_has_claims(person["_id"]),
                        "hasRejects": person_has_reject(person["_id"])
                    }
                    if same_person["locationAddress"] == "":
                        updater["locationAddress"] = get_string_address(person, "locationAddressId")
                    updated = dps["xxx_rpgu_persons"].update_one({"_id": same_person["_id"]}, {"$set": updater})
                    print(iteration, ". [UPDATED]", updated.modified_count)
                else:
                    updater = {
                        "surname": get_attribute(person, "surname"),
                        "firstName": get_attribute(person, "firstName"),
                        "middleName": get_attribute(person, "middleName"),
                        "senderName": "DPS",
                        "dateOfBirth": get_attribute(person, "dateOfBirth"),
                        "email": get_contact(person, "EML"),
                        "phone": get_contact(person, "PHN", "MBT", "CPH"),
                        "locationAddress": get_string_address(person, "locationAddressId"),
                        "workAddress": get_string_address(person, "ipWorkPlaceAddressId"),
                        "hasClaims": person_has_claims(person["_id"]),
                        "hasRejects": person_has_reject(person["_id"]),
                        "socialId": "",
                        "snils": get_attribute(person, "snils"),
                    }
                    inserted = dps["xxx_rpgu_persons"].insert_one(updater)
                    print(iteration, ". [ADDED]", inserted.inserted_id)
        break
    except InvalidBSON as e:
        print(e, iteration)
        iteration += 1

from rldd.client import Client
from rldd import config


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


dps = Client(config.DPS, "dps").connect()
prod = Client(config.PROD).connect()
projection = {
    "surname": 1,
    "firstName": 1,
    "middleName": 1,
    "dateOfBirth": 1,
    "gender": 1,
    "contacts": 1,
    "registrationAddressId": 1
}
iteration = 0
file_num = 1
result_file = open(f"persons{file_num}.csv", "w+", encoding="utf-8")
result_file.write("surname;firstName;middleName;dateOfBirth;gender;registrationAddress;email;phone\n")
persons = dps["persons"].find({"technicalProperties.type": "GOLD", "type": "PHYSICAL"}, projection, no_cursor_timeout=True).limit(10)
for person in persons:
    try:
        iteration += 1
        result = {
            "surname": get_attribute(person, "surname"),
            "firstName": get_attribute(person, "firstName"),
            "middleName": get_attribute(person, "middleName"),
            "dateOfBirth": get_attribute(person, "dateOfBirth"),
            "gender": get_attribute(person, "gender"),
            "registrationAddress": "",
            "email": get_contact(person, "EML"),
            "phone": get_contact(person, "MBT", "PHN")
        }
        registrationAddressId = get_attribute(person, "registrationAddressId")
        if registrationAddressId != '':
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
            address = prod["addresses"].find_one({"_id": Client.getId(registrationAddressId)}, address_projection)
            if address is not None:
                addressObj = {
                    "country": get_prefix(address, "country"),
                    "region": get_prefix(address, "region"),
                    "area": get_prefix(address, "area"),
                    "locality": get_prefix(address, "locality"),
                    "street": get_prefix(address, "street"),
                    "houseNumber": f'д. {get_prefix(address, "houseNumber")}' if get_prefix(address, "houseNumber") != '' else '',
                    "corps": get_prefix(address, "corps"),
                    "room": f'кв. {get_prefix(address, "room")}' if get_prefix(address, "room") != '' else ''
                }
                reg_adr = []
                for adr in list(addressObj.keys()):
                    if addressObj[adr] == '':
                        del addressObj[adr]
                    else:
                        reg_adr.append(addressObj[adr])
                result["registrationAddress"] = ", ".join(reg_adr)
        res_string = ""
        for k in result.keys():
            res_string += result[k] + ";"
        result_file.write(f"{res_string[:-1]}\n")
        if iteration % 1000000 == 0:
            file_num += 1
            result_file.close()
            result_file = open(f"persons{file_num}.csv", "w+", encoding="utf-8")
            result_file.write("surname;firstName;middleName;dateOfBirth;gender;registrationAddress;email;phone\n")

        if iteration % 10000 == 0:
            print(iteration)
    except UnicodeEncodeError as e:
        print(person["_id"], e)

result_file.close()

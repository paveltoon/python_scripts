from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
juridical_file = open('juridical.csv', 'w+')
ip_file = open('ip.csv', 'w+')

juridical_file.write('Фактический адрес;Адрес регистрации;ИНН\n')
ip_file.write('Фактический адрес;Адрес регистрации;ИНН\n')
iteration = 0
claims = db["claims"].find({
    "activationDate": {
        '$gte': Client.ISODate("2018-12-31T21:00:00.000+0000"),
        '$lte': Client.ISODate("2020-12-15T21:00:00.000+0000")},
    "service.srguServicePassportId": {"$in": [
        "5000000000184762039",
        "5000000000183970738"
    ]}})


def form_address(_address):
    _arr = [
        checkValue(_address, "region"),
        checkValue(_address, "street"),
        checkValue(_address, "houseNumber"),
        checkValue(_address, "room")
    ]
    new_arr = list(filter(lambda item: item.strip() != "", _arr))

    return ", ".join(new_arr)


def getAddress(_id):
    _address = db["addresses"].find_one({"_id": Client.getId(_id)})
    if _address:
        if "_class" in _address:
            del _address["_class"]
        return _address
    return ''


def checkValue(obj, val):
    if val in obj:
        return f"{obj[val]}"
    else:
        return ''


for claim in claims:
    iteration += 1

    claimId = claim["_id"]
    ccn = claim["customClaimNumber"]
    print(iteration, ccn)
    if "personsInfo" not in claim:
        continue

    personsInfo = claim["personsInfo"]
    for person in personsInfo:

        if "type" in person:
            if person["type"] == "JURIDICAL":
                result = {
                    'inn': '',
                    'orgJuridicalAddress': '',
                    'orgActualAddress': ''
                }
                if "orgJuridicalAddressId" in person:
                    orgJuridicalAddress = getAddress(checkValue(person, 'orgJuridicalAddressId')) if checkValue(person,
                                                                                                                'orgJuridicalAddressId') != '' else ''
                    result['orgJuridicalAddress'] = form_address(orgJuridicalAddress)

                if "orgActualAddressId" in person:
                    orgActualAddress = getAddress(checkValue(person, 'orgActualAddressId')) if checkValue(person,
                                                                                                          'orgActualAddressId') != '' else ''
                    result['orgActualAddress'] = form_address(orgActualAddress)

                result['inn'] = checkValue(person, 'orgInn')
                juridical_file.write(f"{result['orgActualAddress']};{result['orgJuridicalAddress']};{result['inn']}\n")

            elif person["type"] == "IP":
                result = {
                    'inn': '',
                    'registrationAddress': '',
                    'locationAddress': ''
                }
                if "registrationAddressId" in person:
                    orgJuridicalAddress = getAddress(checkValue(person, 'registrationAddressId')) if checkValue(person,
                                                                                                                'registrationAddressId') != '' else ''
                    result['registrationAddress'] = form_address(orgJuridicalAddress)

                if "locationAddressId" in person:
                    orgActualAddress = getAddress(checkValue(person, 'locationAddressId')) if checkValue(person,
                                                                                                         'locationAddressId') != '' else ''
                    result['locationAddress'] = form_address(orgActualAddress)
                result['inn'] = checkValue(person, 'inn')
                ip_file.write(f"{result['locationAddress']};{result['registrationAddress']};{result['inn']}\n")
juridical_file.close()
ip_file.close()
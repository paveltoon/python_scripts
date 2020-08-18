import json


def checkValues(obj, val):
    if val in obj:
        return f"{obj[val]}"
    else:
        return ''


def getRelations(obj, val):
    func_result = []
    if val in obj:
        for k in obj[val]:
            status = k["relation_subject"]
            s = k["relation_digital_profile"]
            fio = f'{checkValues(s, "lastName")} {checkValues(s, "firstName")} {checkValues(s, "middleName")}'
            func_result.append(f'{status.strip()}: {fio.strip()}')
        return ", ".join(func_result)
    else:
        return ''


def getAddress(obj):
    func_result = []
    if "addresses" in obj:
        for adrs in obj["addresses"]:
            address_type = checkValues(adrs, "address_type")
            fias = "ФИАС отсутствует" if checkValues(adrs, "fias") == "" else checkValues(adrs, "fias")
            kladr = checkValues(adrs, "kladr")
            adr = adrs["address"]
            country = checkValues(adr, "country")
            region = "Московская обл." if checkValues(adr, "region") == "Московская" else checkValues(adr, "region")
            city = checkValues(adr, "city")
            street_address = checkValues(adr, "street_address")
            func_result.append(f'{address_type}: {fias}, {kladr}, {country}, {region}, {city}, {street_address}')
        return ", ".join(func_result)
    else:
        return ''


result_file = open('jsonRes.csv', "a+")
result_file.write("ID;Фамилия;Имя;Отчество;Дата рождения;Пол;Связи;Адрес(Тип, ФИАС, КЛАДР, Страна, Регион, Город и т.д)\n")
res = open('../07-08-2020 20-32-55 836.json', encoding="utf-8")

tojson = json.load(res)
result = []

for pers in tojson:

    needValues = [
        checkValues(pers, "_id"),
        checkValues(pers, "lastName"),
        checkValues(pers, "firstName"),
        checkValues(pers, "middleName"),
        checkValues(pers, "birthDate"),
        checkValues(pers, "gender"),
        getRelations(pers, "relations"),
        getAddress(pers)
    ]
    val_res = ";".join(needValues)
    result_file.write(f'{val_res}\n')
result_file.close()
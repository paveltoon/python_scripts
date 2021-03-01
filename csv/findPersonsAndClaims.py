import csv
from rldd.client import Client
from rldd import config

dps = Client(config.DPS, "dps").connect()
db = Client(config.PROD).connect()


def get_birth_date(_date: str):
    _newDate = _date.split(".")
    if len(_newDate) == 3:
        return f"{_newDate[2]}-{_newDate[1]}-{_newDate[0]}"
    return None


file_num = 3
in_file = open(f'РПГУ{file_num}.csv', 'r+')
reader = csv.reader(in_file, delimiter=";")
out_file = open(f'rpgu_persons{file_num}.csv', 'w+')
out_file.write("ЕСИА Авторизация;Тип Авторизации;Есиа ID\n")
next(reader, None)
for row in reader:
    for index, sym in enumerate(row):
        row[index] = sym.replace("  ", " ")
    isFioInFirstRow = len(row[0].strip().split(' ')) >= 2
    fio = row[0].strip().split(
        " ") if isFioInFirstRow else f"{row[0].strip()} {row[1].strip()} {row[2].strip()}".strip().split(" ")
    dateOfBirth = get_birth_date(row[1].strip()) if isFioInFirstRow else get_birth_date(row[3].strip())
    email = row[2].strip() if isFioInFirstRow else row[4]
    query = {}
    isFound = False
    try:
        if dateOfBirth is not None:
            query = {
                "surname": fio[0],
                "firstName": fio[1],
                "dateOfBirth": dateOfBirth
            }
            if len(fio) >= 3:
                query["middleName"] = fio[2].strip()
        else:
            query = {
                "surname": fio[0],
                "firstName": fio[1],
                "contacts.value": email
            }
            if len(fio) >= 3:
                query["middleName"] = fio[2].strip()
    except KeyError:
        out_file.write(";;\n")
        continue
    except IndexError:
        out_file.write(";;\n")
        continue
    except:
        out_file.write(";;\n")
        continue

    persons = dps["persons"].find(query)
    for person in persons:
        personId = person["_id"]
        esiaAuthorization = True if "esia" in person else False
        if not esiaAuthorization:
            continue
        isFound = True
        esiaId = ""
        esiaType = True if esiaAuthorization else False

        if esiaAuthorization:
            if "authorizationType" in person["esia"]:
                esiaType = person["esia"]["authorizationType"]

        if esiaAuthorization:
            if "id" in person["esia"]:
                esiaId = person["esia"]["id"]

        claimsCount = True if db["claims"].count_documents({"persons": str(personId)}) > 0 else False
        out_file.write(f"{esiaAuthorization};{esiaType};{esiaId}\n")
        print(' '.join(fio), claimsCount, esiaAuthorization, esiaType, esiaId)
        break
    if not isFound:
        out_file.write(";;\n")
print(file_num)

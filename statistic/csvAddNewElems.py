from rldd.client import Client
from rldd import config
import csv

dps = Client(config.DPS, "dps").connect()

in_file = open("persons.csv", "r", newline="")
reader = csv.reader(in_file, delimiter=";")
out_file = open("persons_out.csv", "w", newline="")
writer = csv.writer(out_file, delimiter=";")
header = next(reader, None)
writer.writerow(header + ["senderName", "esiaId", "socialId"])


def format_date(date):
    d = date.split(".")
    return f"{d[2]}-{d[1]}-{d[0]}"


iteration = 0
for row in reader:
    iteration += 1
    surname = row[1]
    firstName = row[2]
    middleName = row[3]
    dateOfBirth = format_date(row[5])
    person = dps["xxx_rpgu_persons"].find_one({
        "surname": surname,
        "firstName": firstName,
        "middleName": middleName,
        "dateOfBirth": dateOfBirth
    })
    if person:
        try:
            writer.writerow(row + [person["senderName"], person["esiaId"], person["socialId"]])
            print(iteration, person["_id"], "[ADDED]")
            continue
        except KeyError as k:
            writer.writerow(row)
            print(person["_id"], k)
            continue

    writer.writerow(row)
    print(iteration, "[SKIPPED]")

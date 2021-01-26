import csv
import datetime

in_file = open("выгрузка 1.csv", "r", newline="", encoding="utf-8")
reader = csv.reader(in_file, delimiter=";")
out_file = open("out.csv", "w", newline="")
writer = csv.writer(out_file, delimiter=";")
next(reader, None)


class ExcelRow:
    def __init__(self, _row):
        self.row = {
            "surname": _row[0],
            "firstName": _row[1],
            "middleName": _row[2],
            "senderName": "RPGU",
            "dateOfBirth": _row[3],
            "email": _row[4],
            "phone": _row[5],
            "locationAddress": _row[6],
            "workAddress": _row[7],
            "hasClaims": _row[8],
            "hasRejects": _row[9],
            "socialId": _row[10],
            "snils": _row[11],
            "regionNumber": ""
        }
        self.format_snils()
        self.format_date_of_birth()

    def get_row(self):
        newArr = []
        for val in self.row.values():
            newArr.append(val)
        return newArr

    def format_snils(self):
        newForm = "".join(self.row["snils"].split("-"))
        self.row["snils"] = "".join(newForm.split(" ")).strip()

    def format_date_of_birth(self):
        self.row["dateOfBirth"] = self.row["dateOfBirth"].replace("/", "-")


for row in reader:
    try:
        r = ExcelRow(row)
        print(r.row)
        writer.writerow(r.get_row())
    except UnicodeEncodeError as u:
        print(u)
        continue
in_file.close()
out_file.close()

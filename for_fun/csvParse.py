import csv

iterat = 0
name_count = 1
result_file = open(f'res_{name_count}.csv', mode='a+', encoding="utf-8")
res = {
    0: "Юр. лицо",
    1: "Фамилия",
    2: "Имя",
    3: "Отчество",
    4: "Дата рождения",
    5: "ADRES",
    6: "AdresFact",
    7: "Наименование документа",  #
    8: "серия",  #
    9: "номер документа",  #
    10: "дата выдачи документа",  #
    11: "контакный телефон",
    12: "почта",
    13: "СНИЛС",  #
    14: "серия полиса",  #
    15: "номер полиса"  #
}
with open('../1111.csv', newline='', encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    for row in csvreader:
        iterat += 1
        print(iterat)
        result_file.write(f"{row[0]};{row[1]};{row[2]};{row[3]};{row[4]};{row[5]};{row[6]};{row[11]};{row[12]}\n")
        if iterat % 500000 == 0:
            name_count += 1
            result_file.close()
            result_file = open(f'res_{name_count}.csv', mode='a+', encoding="utf-8")
            # result_file.write("Юр. лицо;Фамилия;Имя;Отчество;Дата рождения;ADRES;AdresFact;контакный телефон;почта\n")
result_file.close()
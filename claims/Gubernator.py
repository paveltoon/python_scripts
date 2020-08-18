from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
result_file = open("opros.csv", "w+")

ageGroups = {
    '1': {
        "count": 0,
        "summ1": 0,
        "summ2": 0,
        "summ3": 0
    },
    '2': {
        "count": 0,
        "summ1": 0,
        "summ2": 0,
        "summ3": 0
    },
    '3': {
        "count": 0,
        "summ1": 0,
        "summ2": 0,
        "summ3": 0
    },
    '4': {
        "count": 0,
        "summ1": 0,
        "summ2": 0,
        "summ3": 0
    },
}

question = {
    "Оцените работу губернатора Московской области А.Воробьева по шкале от 1 до 10, где 1 – максимально негативно, 10 – максимально позитивно": "summ1",
    "Насколько про Вас можно сказать, что Вы поддерживаете губернатора Московской области А.Воробьева? Оцените по шкале от 1 до 10, где 1-максимальный негатив, не поддерживаю, 10 – максимальный позитив, полностью поддерживаю": "summ2",
    "Насколько про Вас можно сказать, что Вы высказываете, выражаете или отстаиваете свою позицию в отношении губернатора А.Воробьева в личном общении (с родственниками, друзьями, коллегами) или в социальных сетях? по шкале от 1 до 10, где 1 – нет, никогда, 10 – да, всегда": "summ3"
}
result_file.write(f"ОМСУ;Оцените работу губернатора Московской области А.Воробьева по шкале от 1 до 10, где 1 – максимально негативно, 10 – максимально позитивно;Насколько про Вас можно сказать, что Вы поддерживаете губернатора Московской области А.Воробьева? Оцените по шкале от 1 до 10, где 1-максимальный негатив, не поддерживаю, 10 – максимальный позитив, полностью поддерживаю;Насколько про Вас можно сказать, что Вы высказываете, выражаете или отстаиваете свою позицию в отношении губернатора А.Воробьева в личном общении (с родственниками, друзьями, коллегами) или в социальных сетях? по шкале от 1 до 10, где 1 – нет, никогда, 10 – да, всегда;Кол-во\n")


def getOktmo(oktmo):
    oktmoName = db["oktmos"].find_one({"oktmo": str(oktmo)})
    if oktmoName is not None:
        return oktmoName["fullName"]
    else:
        print(oktmo)
        return "Неизвестно"


result = {}
total = db["claims"].count_documents({"service.srguServicePassportId": "1234567890000000000"})
current = 0
claims = db["claims"].find({"service.srguServicePassportId": "1234567890000000000"})
for claim in claims:
    current += 1
    print(f"{current} / {total}")

    if "fields" not in claim:
        continue
    seq = claim["fields"]["sequenceValue"]
    omsuName = getOktmo(claim["oktmo"])

    if omsuName == "Неизвестно":
        continue

    if omsuName not in result:
        result[omsuName] = {}
        result[omsuName]["count"] = 0
    print(result[omsuName])
    result[omsuName]["count"] += 1
    ageVal = None
    for el in seq:
        title = el["title"]
        if title == "Информация о респонденте:":
            manSeq = el["sequenceValue"]
            for man in manSeq:
                if man["title"] == "Возраст":
                    ageVal = man["mapValue"]["selected_value"]["value"]
                    ageGroups[ageVal]["count"] += 1
    for el in seq:
        title = el["title"]
        if title in question:
            val = el["value"]
            ageGroups[ageVal][question[title]] += int(val)
            if question[title] not in result[omsuName]:
                result[omsuName][question[title]] = int(val)
            else:
                result[omsuName][question[title]] += int(val)
for key, value in result.items():
    value["summ1"] = float("{0:.1f}".format(value["summ1"]/value["count"]))
    value["summ2"] = float("{0:.1f}".format(value["summ2"]/value["count"]))
    value["summ3"] = float("{0:.1f}".format(value["summ3"]/value["count"]))
    result_file.write(f"{key};{str(value['summ1'])};{str(value['summ2'])};{str(value['summ3'])};{str(value['count'])}\n")
result_file.write(f"\nВозрастная группа;;Оцените работу губернатора Московской области А.Воробьева по шкале от 1 до 10, где 1 – максимально негативно, 10 – максимально позитивно;Насколько про Вас можно сказать, что Вы поддерживаете губернатора Московской области А.Воробьева? Оцените по шкале от 1 до 10, где 1-максимальный негатив, не поддерживаю, 10 – максимальный позитив, полностью поддерживаю;Насколько про Вас можно сказать, что Вы высказываете, выражаете или отстаиваете свою позицию в отношении губернатора А.Воробьева в личном общении (с родственниками, друзьями, коллегами) или в социальных сетях? по шкале от 1 до 10, где 1 – нет, никогда, 10 – да, всегда;Кол-во\n")
for key, value in ageGroups.items():
    value["summ1"] = float("{0:.1f}".format(value["summ1"]/value["count"]))
    value["summ2"] = float("{0:.1f}".format(value["summ2"]/value["count"]))
    value["summ3"] = float("{0:.1f}".format(value["summ3"]/value["count"]))
    result_file.write(f"{key};{str(value['summ1'])};{str(value['summ2'])};{str(value['summ3'])};{str(value['count'])}\n")
print(ageGroups)
result_file.close()


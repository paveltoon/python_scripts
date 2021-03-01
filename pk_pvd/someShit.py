from rldd.client import Client
from rldd.config import PKPVD

db = Client(PKPVD, "pvdrs").connect()
result_file = open('result.csv', 'w+', encoding='utf-8')
currentStepDecode = {
    "CREATE": "Приём обращения",
    "FORMING": "Формирование обращения",
    "ATTACH_IMAGE": "Присоединение образов",
    "PPOZ_STATEMENT_PROCESS": "Обработка обращения в ППОЗ",
    "PPOZ_DOC_PROCESS": "Обработка пакета документов в ППОЗ",
    "EDIT": "Корректировка обращения",
    "DOC_BACK_9": "Возврат документов",
    "BACK_POST_10": "Возврат по почте",
    "WAIT_OUT_11": "Ожидается выдача",
    "BACK_UP_12": "Возврат осуществлён",
    "PROCESS_END_13": "Обработка завершена",
    "CORRECT_IMAGE_14": "Корректировка образов",
    "PPOZ_STATEMENT_PROBLEM": "Проблемы отправки пакета заявлений",
    "PPOZ_DOC_PROBLEM": "Проблемы отправки пакета документов",
    "SEND_STATEMENT_17": "Отправка пакета заявлений",
    "SEND_DOC_18": "Отправка пакета документов",
    "REFUSED_STATEMENT_19": "ППОЗ отказал в приёме пакета заявлений",
    "REFUSED_DOC_20": "ППОЗ отказал в приёме пакета документов",
    "SENDING_OUT_21": "Передача сообщения о возврате, выдаче",
    "WAIT_CONFIRM_24": "Ожидание подтверждения пакета заявлений",
    "PKG_STM_READY_30": "Пакет заявлений готов к отправке",
    "PKG_STM_PROCESS_31": "Отправка пакета заявлений",
    "PKG_STM_PROBLEM_32": "Проблемы с отправкой пакета заявлений",
    "PKG_STM_WAIT_CONFIRM_33": "Ожидание проверки пакета заявлений в ППОЗ",
    "PKG_STM_RETURN_REJECT_34": "ППОЗ отказал в приёме пакета заявлений",
    "PKG_IMG_READY_40": "Пакет документов готов к отправке",
    "PKG_IMG_PROCESS_41": "Отправка пакета документов",
    "PKG_IMG_PROBLEM_42": "Проблемы с отправкой пакета документов",
    "PKG_IMG_WAIT_PPOZ_43": "Обработка документов в ППОЗ",
    "PKG_IMG_RETURN_REJECT_44": "ППОЗ отказал в приёме пакета документов",
    "CANCELED_114": "Аннулировано",
    "ABNORMAL_TERMINATION_115": "Аварийное завершение"
}

result_file.write(
    "Дата создания;Код МФЦ;Наименование МФЦ;Номер обращения;Номер заявления;Количество;Заявители;Оператор приема;Наименование услуги\n")
query = {
    "createEvent.dateWhen": {
        "$gte": Client.ISODate("2020-06-10T00:00:00.000+0300"),
        "$lte": Client.ISODate("2021-01-01T00:00:00.000+0300")
    },
    "currentStep": {
        "$nin": ["CANCELED_114", "CREATE", "ATTACH_IMAGE"]
    },
    "name": {"$nin": ["Предоставление копии документов из реестрового дела объекта недвижимости",
                      "Предоставление копии документов из реестрового дела зоны, территории или границ",
                      "Предоставление сведений об объекте недвижимости", "Предоставление сведений о правообладателе",
                      "Предоставление сведений о кадастровом квартале", "Предоставление сведений о зоне",
                      "Предоставление сведений о границе", "Предоставление сведений доступом к ФГИС ЕГРН",
                      "Предоставление аналитической информации", "Предоставление перечня для ГКО",
                      "Возврат платы за предоставление сведений, содержащихся в ЕГРН, иной информации",
                      "Дополнительные документы"]}
}
iteration = 0
docs = db["rs_appeal"].find(query)

total = db["rs_appeal"].count_documents(query)
for doc in docs:
    iteration += 1
    try:
        dateWhen = doc["createEvent"]["dateWhen"] if "dateWhen" in doc["createEvent"] else ''
        internalNum = doc["internalNum"]
        orgCode = doc["createEvent"]["performer"]["orgCode"]
        orgName = doc["createEvent"]["performer"]["orgName"]
        orgName.replace('\n', "")

        textApplicants = doc["textApplicants"]
        createdWho = doc["createdWho"]
        statements = doc["statements"]
        statementsArr = []
        claimsCount = 0
        for s in statements:
            statementsArr.append(s["internalNum"])
            claimsCount += 1

        name = doc["name"]
        print(f"{internalNum}. {iteration} / {total}")
        result_file.write(f"{dateWhen};{orgCode};{orgName};{internalNum};{', '.join(statementsArr)};{claimsCount};{textApplicants};{createdWho};{name}\n")
    except KeyError:
        continue

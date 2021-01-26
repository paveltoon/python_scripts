from xml.dom import minidom
import os

from bson import ObjectId


def getId(_id):
    if len(_id) == 24:
        return ObjectId(_id)
    else:
        return _id


wrong_file = open("wrong_data.csv", "w+")
result_file = open("data.csv", "w+")
result_file.write("claimId;personType;snils;inn;ogrn;kpp\n")
file_list = os.listdir("./files")
for doc in file_list:
    isWrong = True
    path = f"files/{doc}"
    size = os.path.getsize(path)
    if size / (1024 * 1024) < 20:
        file = open(path, encoding='utf-8')
        dom = minidom.parse(file)
        claimId = getId("".join("".join("".join(file.name.split("files/req_")).split(".xml")).split("(1)")).strip())
        dom.normalize()
        applicantType = dom.getElementsByTagName("ns2:applicantType")[0].childNodes[0].data if dom.getElementsByTagName(
            "ns2:applicantType") else None
        trusteeType = dom.getElementsByTagName("ns2:trusteeType")[0].childNodes[0].data if dom.getElementsByTagName(
            "ns2:trusteeType") else None

        if applicantType == "IP" or applicantType == "FL":
            snils = dom.getElementsByTagName("ns2:snils")[0].childNodes[0].data.replace("-", "").replace(" ",
                                                                                                         "").strip()
            isWrong = False
            result_file.write(f"{claimId};{applicantType};{snils}\n")
            print(applicantType, claimId, snils)
        elif applicantType == "UL":
            isWrong = False
            inn = dom.getElementsByTagName("ns2:inn")[0].childNodes[0].data if len(
                dom.getElementsByTagName("ns2:inn")) > 0 and len(
                dom.getElementsByTagName("ns2:inn")[0].childNodes) > 0 else \
            dom.getElementsByTagName("ns2:innUPD")[0].childNodes[0].data
            ogrn = dom.getElementsByTagName("ns2:ogrn")[0].childNodes[0].data if len(
                dom.getElementsByTagName("ns2:ogrn")) > 0 and len(
                dom.getElementsByTagName("ns2:ogrn")[0].childNodes) > 0 else \
                dom.getElementsByTagName("ns2:ogrnUPD")[0].childNodes[0].data
            kpp = dom.getElementsByTagName("ns2:kpp")[0].childNodes[0].data
            result_file.write(f"{claimId};{applicantType};;{inn};{ogrn};{kpp}\n")
            print(applicantType, inn, ogrn, kpp)

        if trusteeType == "IP" or trusteeType == "FL":
            isWrong = False
            snilsTrust = dom.getElementsByTagName("ns2:snilsTrust")[0].childNodes[0].data.replace("-", "").replace(" ",
                                                                                                                   "").strip()
            result_file.write(f"{claimId};{trusteeType + 'Trust'};{snilsTrust}\n")
            print(trusteeType + "Trust", claimId, snilsTrust)
        elif trusteeType == "UL":
            isWrong = False
            innTrust = dom.getElementsByTagName("ns2:innTrust")[0].childNodes[0].data if dom.getElementsByTagName(
                "ns2:innTrust") else \
                dom.getElementsByTagName("ns2:innUPDTrust")[0].childNodes[0].data
            ogrnTrust = dom.getElementsByTagName("ns2:ogrnTrust")[0].childNodes[0].data if dom.getElementsByTagName(
                "ns2:ogrnTrust") else \
                dom.getElementsByTagName("ns2:ogrnUPDTrust")[0].childNodes[0].data
            kppTrust = dom.getElementsByTagName("ns2:kppTrust")[0].childNodes[0].data
            result_file.write(f"{claimId};{trusteeType + 'Trust'};;{innTrust};{ogrnTrust};{kppTrust}\n")
            print(trusteeType + "Trust", innTrust, ogrnTrust, kppTrust)

        if isWrong:
            wrong_file.write(f"{claimId}\n")
        file.close()

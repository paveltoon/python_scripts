from rldd.client import Client


class Person:
    def __init__(self, _person, _db):
        self.__person = _person
        if "_class" in self.__person:
            del self.__person["_class"]

        self.__db = _db

    def set_doc_from_id(self, document_param, db_name) -> None:
        if document_param in self.__person:
            document_id = str(self.__person[document_param])
            document_name = document_param[:document_param.rfind('Id')]
            doc = self.__db[db_name].find_one({"_id": Client.getId(document_id)})
            if doc:
                if "_class" in doc:
                    del doc["_class"]
                self.__person[document_name] = doc

    def form_person_to_claim(self) -> None:
        self.set_doc_from_id("currIdentityDocId", "docs")
        self.set_doc_from_id("registrationAddressId", "addresses")
        self.set_doc_from_id("locationAddressId", "addresses")
        self.set_doc_from_id("ipWorkPlaceAddressId", "addresses")

    def get_id(self):
        return self.__person["_id"]

    def get_attr(self, atr_name):
        if atr_name in self.__person:
            return self.__person[atr_name]
        return None

    def get_fio(self):
        result_str = ""
        result_str += self.get_attr("surname")
        result_str += " " + self.get_attr("firstName")
        result_str += " " + self.get_attr("middleName")
        if result_str.strip() == "":
            return None
        return result_str

    def get_full_person(self) -> dict:
        return self.__person

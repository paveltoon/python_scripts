from rldd import rldd2
from user import rldd_user

import requests

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)


class ProvLevel:

    def __init__(self, srgu_id, prov_level):
        self.srgu_id = str(srgu_id)
        self.prov_level = prov_level
        self.dictionary = db["dictionaries"].find_one({"dictionaryName": "provLevel"})
        self.dict_id = self.dictionary["_id"]

    def update(self, prov_level_type):
        updater = {}
        for index, level in enumerate(self.dictionary["sections"]):
            if level["sectionName"] == prov_level_type:
                definitions = level["definitions"]
                if self.srgu_id not in definitions:
                    definitions[self.srgu_id] = self.prov_level
                    updater[f"sections.{index}.definitions"] = definitions
                    upd = db["dictionaries"].update_one({"_id": self.dict_id}, {"$set": updater})
                    return {"status": True, "modified": upd.modified_count, "matched": upd.matched_count}
                else:
                    return {"status": False}

    def addPassportId(self):
        update = self.update("srguServicePassportId")
        if update["status"] is True:
            patch = self.Patch_nodes()
            print(f"Dictionary has been updated. Progress: {update['modified']} / {update['matched']}")
            print(patch)
        else:
            print(f"[INFO] PassportId {self.srgu_id} already exists.")

    def addServiceId(self):
        update = self.update("srguServiceId")
        if update["status"] is True:
            patch = self.Patch_nodes()
            print(f"Dictionary has been updated. Progress: {update['modified']} / {update['matched']}")
            print(patch)
        else:
            print(f"[INFO] ServiceId {self.srgu_id} already exists.")

    @staticmethod
    def Patch_nodes():
        servers = [
            "10.10.80.86",
            "10.10.80.87",
            "10.10.80.88",
            "10.10.80.89",
            "10.10.80.90",
            "10.10.80.163",
        ]
        statuses = []
        for server in servers:
            url = f"http://{server}:8080/api/dictionaries/"
            response = requests.request("PATCH", url)
            if 200 <= response.status_code <= 300:
                statuses.append("ok")
            else:
                statuses.append("error")
        if "error" in statuses:
            return "error"
        else:
            return "ok"


ProvLevel("5000000010000015328", "Региональный").addPassportId()

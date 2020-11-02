from rldd.client import Client
from rldd import config
import csv

db = Client(config.PROD).connect()

with open("dbNameMfc.csv", newline='') as csvfile:
    codes = csv.reader(csvfile, delimiter=";")
    for row in codes:
        dept = row[0]
        remote = Client(config.REMOTE, dept).connect()
        orgcard = remote["orgcard"].find_one()["armsCaption"]
        upd = db["deptcodes"].update_one({"deptId": dept}, {"$set": {"deptId": dept, "name": orgcard}}, upsert=True)
        print(f"{dept} has been updated. process: {upd.modified_count} / {upd.matched_count}")

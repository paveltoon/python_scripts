from bson import DBRef

from rldd.client import Client
from rldd import config

servicesIds = [
    "53fdca4b6fcd6174c4e5d8a6"
]
db_list = Client(config.REMOTE, '').get_db_list()
main_base = Client(config.REMOTE, 'mfc-work').connect()
for dbName in db_list:
    if dbName.startswith('mfc'):
        db = Client(config.REMOTE, dbName).connect()
        collection_list: list = db.list_collection_names()
        for coll in collection_list:
            if coll == "doc_dss_tags":
                for serv_id in servicesIds:
                    doc_dss_tags = main_base["doc_dss_tags"].find({"service": DBRef("services", Client.getId(serv_id))})
                    service = main_base["services"].find_one({"_id": Client.getId(serv_id)})
                    if service:
                        inDocsItems = service["inDocsItems"]
                        in_docs = service["in_docs"]
                        for doc in in_docs:
                            docId = doc.id
                            collection = doc.collection
                            main_doc = main_base[collection].find_one({"_id": docId})
                            if main_doc:
                                del main_doc["_id"]
                                db[collection].update_one({"_id": docId}, {"$set": main_doc}, upsert=True)
                        db["services"].update_one({"_id": Client.getId(serv_id)}, {"$set": {"in_docs": in_docs, "inDocsItems": inDocsItems}})
                    for doc_dss_tag in doc_dss_tags:
                        dss_id = doc_dss_tag["_id"]
                        del doc_dss_tag["_id"]
                        db["doc_dss_tags"].update_one({
                            "_id": dss_id
                        }, {
                            "$set": doc_dss_tag
                        },
                            upsert=True
                        )
                    print(dbName, "updated")

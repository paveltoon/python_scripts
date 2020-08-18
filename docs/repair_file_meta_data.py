from rldd import rldd2
from user import rldd_user
from bson import ObjectId

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
docs = db["docs"].find({"fileMetadata._id": {"$in": [ObjectId("5e7b69f0352df30001d4f205")]}})
for doc in docs:
    docId = doc["_id"]
    try:
        fileMetadata = doc["fileMetadata"]
        dataId = fileMetadata["_id"]
        data = db["alt.files"].find_one({"_id": dataId})
        if data is None:
            if len(fileMetadata["md5"]) == 32:
                ins = db["alt.files"].insert_one(fileMetadata)
                print(f"FileMetadata has been added with id: {fileMetadata['_id']}.")

    except KeyError as e:
        print(docId, "has no key:", e)
    except:
        print("[ERROR]", docId)

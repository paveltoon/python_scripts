from rldd import rldd2
from user import rldd_user

db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
docs = db["docs"].find({ "createDate": { "$gte": rldd2.ISODate("2020-02-29T21:00:00.000+0000") }, "fileMetadata._id": { "$exists": True } }).limit(10)
for doc in docs:
    docId = doc["_id"]
    try:
        fileMetadata = doc["fileMetadata"]
        dataId = fileMetadata["_id"]
        data = db["alt.files"].find_one({"_id": dataId})
        if data is None:
            if data is None:
                pass
                # ins = db["alt.files"].insert_one(fileMetadata)
                # print(f"FileMetadata has been added with id: {fileMetadata['_id']}.")

    except KeyError as e:
        print(docId, "has no key:", e)

from datetime import datetime, timedelta
from rldd.client import Client
from rldd import config

from_date = datetime.now() - timedelta(days=30)
db = Client(config.PROD).connect()
mkus = db["claims_status_mku"].delete_many({"createDate": {"$lte": from_date}})
print(f"Docs deleted: {mkus.deleted_count}")

from rldd.client import Client
from rldd.config import PROD

from statuses.newIntegrationTest import create_status, send_file, create_doc, update_status

db = Client(PROD).connect()
statusId = "603f84e0799ab5000154eae6"
sendFile1 = send_file("empty.txt")
docId = create_doc(statusId, "STATUS", "empty.txt", sendFile1)
print(sendFile1)
print(docId)
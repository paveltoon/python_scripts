from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()
claims = db["claims"].find({"customClaimNumber": {"$in": [
    "P001-4348056490-39341692",
    "P001-7297092658-39351186",
    "P001-4493563327-39307296",
    "P001-0736662582-39342147",
    "P001-7545241440-39348799",
    "P001-5699640220-39334170",
    "P001-6719031661-39165262",
    "P001-3403768976-39334242",
    "P001-3397689046-39288524",
    "P001-3397689046-39349605",
    "P001-0450998166-39328159",
    "P001-0413148990-39215341",
    "P001-8469871698-39165577",
    "P001-4382210872-39368532",
    "P001-2648944542-39341952",
    "P001-8099360727-39343229",
    "P001-7297092658-39373006",
    "P001-7238400232-39338878",
    "P001-6937524799-39297294",
    "P001-3397689046-39350493",
    "P001-5318475662-39206977",
    "P001-0016508280-39291500"
]}})
for claim in claims:
    ccn = claim["customClaimNumber"]
    claimId = claim["_id"]
    deadlineDate = claim["deadlineDate"]
    if "docSendDate" in claim:
        upd = db["claims"].update_one({"_id": claimId}, {"$set": {"docSendDate": deadlineDate, "daysToDeadline": 1}})
        print(f"Claim: {ccn}, progress: {upd.modified_count} / {upd.matched_count}")

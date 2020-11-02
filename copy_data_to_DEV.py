from rldd.client import Client
from rldd import config

prod = Client(config.PROD).connect()
dev = Client(config.DEV).connect()
dps = Client(config.DPS, "dps").connect()
dps_dev = Client(config.DPS_DEV, "dps-develop").connect()

addresses_types = [
    "registrationAddressId",
    "locationAddressId",
    "ipWorkPlaceAddressId",
    "birthAddressId"
]

ccn = "M503-3446530994-7523909"


def get_trusted_persons(claim):
    persons = []
    if "trustedPersons" in claim:
        for person in claim["trustedPersons"]:
            persons.append(Client.getId(str(person["trustedPerson"]["trustedId"])))
    data = get_data_from_db(persons)
    return data


def get_persons(claim):
    persons = []
    if "personsInfo" in claim:
        for person in claim["personsInfo"]:
            persons.append(person["_id"])
    data = get_data_from_db(persons)
    return data


def get_data_from_db(ids):
    persons_list = []
    addresses_ids = []
    documents = []
    persons = dps["persons"].find({"_id": {"$in": ids}})
    for person in persons:
        persons_list.append(person)
        documents = get_person_documents(
            Client.getId(person["currIdentityDocId"])) if "currIdentityDocId" in person else []
        for ad in addresses_types:
            if ad in person:
                addresses_ids.append(Client.getId(person[ad]))
    addresses = get_addresses(addresses_ids)
    return {"persons": persons_list, "documents": documents, "addresses": addresses}


def get_statuses(claim_id):
    data = []
    _statuses = prod["claims_status"].find({"claimId": str(claim_id)})
    for _status in _statuses:
        data.append(_status)
    return data


def get_claim_documents(claim_id):
    data = []
    documents = prod["docs"].find({"ownerId": str(claim_id)})
    for _doc in documents:
        data.append(_doc)
    return data


def get_person_documents(_id):
    data = []
    documents = prod["docs"].find({"_id": _id})
    for _doc in documents:
        data.append(_doc)
    return data


def get_addresses(ids):
    data = []
    addresses = prod["addresses"].find({"_id": {"$in": ids}})
    for address in addresses:
        data.append(address)
    return data


def insert_data_to_dev(data_base, data):
    count = 0
    if dev[data_base].find_one({"_id": data["_id"]}) is None:
        dev[data_base].insert_one(data)
        count += 1
    return count


def change_dps_dev_person_by_snils(snils):
    data = dps_dev["persons"].find_one({"snils": snils})
    _result = None
    if data is not None:
        _result = dps_dev["persons"].update_one({"_id": data["_id"]}, {"$unset": {"snils": ""}})
    return _result


def insert_data_to_dps_dev(data):
    snils = data["snils"] if "snils" in data else None
    if snils is not None:
        change_dps_dev_person_by_snils(snils)

    count = 0
    print(data)
    if dps_dev["persons"].find_one({"_id": data["_id"]}) is None:
        dps_dev["persons"].insert_one(data)
        count += 1
    return count


def check_and_insert_docs(data):
    inserted_docs = 0

    if len(data["persons"]) > 0:
        for pers in data["persons"]:
            inserted_docs += insert_data_to_dps_dev(pers)
    if len(data["addresses"]) > 0:
        for address in data["addresses"]:
            inserted_docs += insert_data_to_dev("addresses", address)
    if len(data["documents"]) > 0:

        print(data["documents"])
        for docs in data["documents"]:
            inserted_docs += insert_data_to_dev("docs", docs)

    return inserted_docs


claim_to_copy = prod["claims"].find_one({"customClaimNumber": ccn})

trusted_persons_data = get_trusted_persons(claim_to_copy)
persons_data = get_persons(claim_to_copy)

trusted_persons_result = check_and_insert_docs(trusted_persons_data)
persons_result = check_and_insert_docs(persons_data)

if dev["claims"].find_one({"_id": claim_to_copy["_id"]}) is None:
    upd_claim = dev["claims"].insert_one(claim_to_copy)

claim_docs = get_claim_documents(claim_to_copy["_id"])
if len(claim_docs) > 0:
    for doc in claim_docs:
        insert_data_to_dev("docs", doc)

statuses = get_statuses(claim_to_copy["_id"])

status_count = 0
if len(statuses) > 0:
    for status in statuses:
        status_count += insert_data_to_dev("claims_status", status)

print(f"Added {trusted_persons_result} Trusted Person docs; {persons_result} Person docs; {status_count} Statuses;")
# print("Press ENTER to exit.")
# keyboard.wait('Enter')

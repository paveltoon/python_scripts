from rldd import rldd2
from user import rldd_user


def formatSnils(snils_num):
    formatted = snils_num.split('-')
    new_snils = ''.join(formatted).split(' ')
    return ''.join(new_snils)


db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
# db = rldd2.LOCAL_connect('local')
persons = db['persons'].find({"snils": {"$regex": '.*-.*'}}).limit(300)
for person in persons:
    person_id = person['_id']
    snils = person['snils']
    formatted_snils = formatSnils(snils)
    if formatted_snils == '':
        continue

    try:
        same_persons = db['persons'].find({'snils': formatted_snils})
        same_persons_count = db['persons'].count_documents({'snils': formatted_snils})
        if same_persons_count:
            if same_persons_count > 1:
                print(f'[ERROR] Persons with snils {formatted_snils} more than 1. Skipped')
                continue
            else:
                same_person = same_persons[0]
                if person['surname'] != same_person['surname'] and person['firstName'] != same_person['firstName']:
                    print(f'[ERROR] Persons are different. Snilses {formatted_snils} & {snils}. Skipped.')
                    continue
                else:
                    update_dict = {}
                    personCorrected = False
                    print(snils, formatted_snils)
                    for key in person.keys():
                        if key not in same_person:
                            update_dict[key] = person[key]
                            personCorrected = True
                    if personCorrected:

                        # Find claims and update person
                        if db['claims'].count_documents({"persons": person_id}):
                            claims = db['claims'].find({"persons": person_id})
                            for claim in claims:
                                print(claim['customClaimNumber'])
                        # Update Person
                        update_dict['oldPersonId'] = person_id
                        print(update_dict)
        else:
            print(f'[WARNING] Do not match person with snils: {formatted_snils} & {snils}')
    except KeyError as key_err:
        print(f'[ERROR] Person {formatted_snils} has KeyError. {key_err}')
    except Exception as err:
        print(f'[ERROR] Person {formatted_snils} has Error. {err}')

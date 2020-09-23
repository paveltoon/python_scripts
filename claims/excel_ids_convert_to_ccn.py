import csv
from rldd.client import Client
from rldd import config

db = Client(config.PROD).connect()


class Converter:
    iteration = 0
    result_file = open('ccns.txt', "w+")

    def get_claim_number(self, _id):
        claim = db["claims"].find_one({"_id": Client.getId(_id)})
        return claim["customClaimNumber"]

    def save_from_file(self, _file_name):
        with open(_file_name) as postfile:
            postreader = csv.reader(postfile, delimiter=';')
            for row in postreader:
                self.iteration += 1
                result = self.get_claim_number(row[0])
                print(self.iteration, result)
                self.result_file.write(f'{result}\n')

    def close_file(self):
        self.result_file.close()


file = Converter()
file.save_from_file('post.csv')
file.save_from_file('post_5000000000184562222.csv')
file.save_from_file('pre.csv')
file.close_file()

import datetime
import json

import pymongo
import requests
from bson import ObjectId


class Client:
    def __init__(self, conf, data_base="rldd2"):
        self.__url = conf["post_url"]
        self.__mongodb = conf["mongodb"]
        self.__data_base = data_base

    def connect(self):
        client = pymongo.MongoClient(f"mongodb://{self.__mongodb}")
        if self.__data_base != '':
            return client[self.__data_base]
        else:
            return client

    def postStatus(self, claim_id, status_code,
                   comment="Статус создан автоматически через РЛДД"):
        url = f'http://{self.__url}/api/statuses/'

        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "claimId": str(claim_id),
            "statusCode": str(status_code),
            "createBy": "rldd2",
            "comment": comment,
            "lastModifiedBy": "rldd2",
            "createState": "COMPLETED"
        }
        return requests.request("POST", url=url, headers=headers, data=json.dumps(body))

    @staticmethod
    def ISODate(date):
        full_format = str(date).split('T')
        date_format = full_format[0].split('-')
        for dt_index, dt in enumerate(date_format):
            date_format[dt_index] = str(int(dt))

        time_format = full_format[1].split(':')
        sec = time_format[2].split('.')
        m_sec = ''.join(sec[1].split('+'))
        m_sec_format = m_sec[0:-1]
        time_format[2] = sec[0]
        time_format.append(m_sec_format)

        for tm_index, tm in enumerate(time_format):
            time_format[tm_index] = str(int(tm))
        return datetime.datetime(int(date_format[0]),
                                 int(date_format[1]),
                                 int(date_format[2]),
                                 int(time_format[0]),
                                 int(time_format[1]),
                                 int(time_format[2]),
                                 int(time_format[3]))

    @staticmethod
    def getId(_id):
        if len(_id) == 24:
            return ObjectId(_id)
        else:
            return _id

import pymongo
import datetime


def PROD_connect(login, password, db="rldd2"):
    client = pymongo.MongoClient(f"mongodb://{login}:{password}@10.10.80.31:27017/rldd2")
    return client[db]


def DEV_connect():
    client = pymongo.MongoClient(f"mongodb://rlddService:1q2w3e4r@10.10.80.20:27018/rldd2")
    return client["rldd2"]


def STAGE_connect():
    client = pymongo.MongoClient(f"mongodb://rlddService:1q2w3e4r@10.10.80.21:27018/rldd2")
    return client["rldd2"]


def LOCAL_connect(base_name):
    client = pymongo.MongoClient("localhost:27017")
    return client[base_name]


def isodate(date):
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

from user import rldd_user

PROD = {
    "post_url": "10.10.80.54:8080",
    "mongodb": f"{rldd_user.login}:{rldd_user.pwd}@10.10.80.31:27017/rldd2"
}

DEV = {
    "post_url": "10.10.80.20",
    "mongodb": "rlddService:1q2w3e4r@10.10.80.20:27018/rldd2"
}

STAGE = {
    "post_url": "10.10.80.21",
    "mongodb": "rlddService:1q2w3e4r@10.10.80.21:27018/rldd2"
}

REMOTE = {
    "post_url": "10.10.80.100",
    "mongodb": "10.10.80.100:27017"
}

DPS = {
    "post_url": "eisgmu-dps-db-01:27017",
    "mongodb": f"{rldd_user.login}:{rldd_user.pwd}@eisgmu-dps-db-01:27017/dps"
}

DPS_DEV = {
    "post_url": "eisgmu-services-db-dev:27018",
    "mongodb": "eisgmu-services-db-dev:27018/dps"
}

replicaSET = {
    "post_url": "",
    "mongodb": "10.10.80.140:27017"
}

PKPVD = {
    "post_url": "",
    "mongodb": f"{rldd_user.pvd_login}:{rldd_user.pvd_password}@10.50.109.227:27017/pvdrs"
}

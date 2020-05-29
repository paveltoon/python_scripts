from rldd import rldd2
from user import rldd_user
db = rldd2.PROD_connect(rldd_user.login, rldd_user.pwd)
persons = db['persons']
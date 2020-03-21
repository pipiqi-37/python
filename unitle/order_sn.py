from datetime import datetime
import random


def order_sn():
    now_time = datetime.now()
    str_time = now_time.strftime('%Y%m%d%H%M%S%F')
    return str_time + str(random.randint(1000, 9999))

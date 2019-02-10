import datetime
from pytz import timezone

test = "2019-01-30T09:15:00Z"


def get_time():
    now = datetime.datetime.utcnow()
    return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0] + 'Z'


print(get_time())

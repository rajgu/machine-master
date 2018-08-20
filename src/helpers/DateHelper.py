from datetime import datetime
from datetime import timedelta

class DateHelper:


    def __init__(self):
        return None


    def getCurrentDateTime(self):
        return str(datetime.now())[0:19]


    def getDateTimeDelta(self, delta):
        if delta < 0:
            return str(datetime.now() + timedelta(delta))[0:19]
        else:
            return str(datetime.now() - timedelta(delta))[0:19]


from datetime import datetime

class Getstuff():
    def getdttm(self):
        dttm = datetime.now()
        dt = (str(dttm.year) + "-" + str(dttm.month) + "-" + str(dttm.day)).encode('utf-8')
        tm = (str(dttm.hour) + ":" + str(dttm.minute) + ":" + str(dttm.second)).encode('utf-8')
        return(dt, tm)

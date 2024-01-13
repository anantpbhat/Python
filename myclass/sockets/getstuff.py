
from datetime import datetime

class Getstuff():
    def getdttm(self):
        dttm = datetime.now()
        dt = (str(dttm.year) + "-" + str("%02d" % dttm.month) + "-" + str("%02d" % dttm.day)).encode('utf-8')
        tm = (str("%02d" % dttm.hour) + ":" + str("%02d" % dttm.minute) + ":" + str("%02d" % dttm.second)).encode('utf-8')
        return(dt, tm)

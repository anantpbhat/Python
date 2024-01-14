
### Return Date & Time in String and Binary formats.

from datetime import datetime

class Getstuff():
    def getdttm(self):
        dttm = datetime.now()
        dt = str(dttm.year) + "-" + str("%02d" % dttm.month) + "-" + str("%02d" % dttm.day)
        tm = str("%02d" % dttm.hour) + ":" + str("%02d" % dttm.minute) + ":" + str("%02d" % dttm.second)
        return(dt, tm, (dt, tm).encode('utf-8'))

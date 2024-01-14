
### Write any message provided as Arg1 to a logfile mentioned in Arg2.

class LogIt():
    def wrtnow(self, stmt, logfile):
        with open(logfile, 'a') as lfl:
            print(stmt)
            lfl.write("%s\n" % stmt)
        return

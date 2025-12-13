"""Common class and functions that are ready to be imported"""

from datetime import datetime
import re, sys, getpass

class GetDateTime():
    """Class to provide Date and Time"""
    def __init__(self):
        self.dttm = datetime.now()
        self.dt = str(self.dttm.year) + "-" + str(f"{self.dttm.month:02d}") + "-" + str(f"{self.dttm.day:02d}")
        self.hm = str(f"{self.dttm.hour:02d}") + str(f"{self.dttm.minute:02d}")
        self.hms = self.hm + str(f"{self.dttm.second:02d}")
        self.dow = int(self.dttm.strftime("%w"))                #Convert to int to remove leaving zeros
        self.dom = str(self.dttm.day)
        self.doy = int(self.dttm.strftime("%j"))                #Convert to int to remove leaving zeros
        self.woy = int(self.dttm.strftime("%W"))                #Convert to int to remove leaving zeros
        self.moy = str(self.dttm.month)
        self.fyr = str(self.dttm.year)

    def getdthm(self):
        """Provides date & time without seconds in string text"""
        return(self.dt, self.hm)
    
    def getdthms(self):
        """Provides date & time with seconds in string text"""
        return(self.dt, self.hms)
    
    def getdthmbin(self):
        """Provides date & time without seconds in binary"""
        return(self.dt.encode('utf-8'), self.hm.encode('utf-8'))
    
    def getdow(self):
        """Provides day of week 1 - 7"""
        return str(self.dow)
    
    def getdom(self):
        """Provides day of month 1 - 31"""
        return self.dom
    
    def getdoy(self):
        """Provides day of week 1 - 366"""
        return str(self.doy)
    
    def getwoy(self):
        """Provides day of week 1 -53"""
        return str(self.woy)
        
    def getmoy(self):
        """Provides month of year 1 - 12"""
        return self.moy

    def getfyr(self):
        """Provides Full year inm long form"""
        return self.fyr
    
class AssignArgInput():
    """Assign value from cmdline args or prompt user for one"""
    def __init__(self, arg1="Value", arg2=None):
        self.ask = arg1
        self.val = arg2
        self.qp = re.compile(r'^q$|^quit$', re.I)

    def assignit(self):
        """Function to assign string value from arg or ask for input"""
        if self.val:
            VAL = self.val
        else:
            VAL = input(f"Enter {self.ask} here or (q|Q) to quit: ")
            if self.qp.search(VAL):
                print("Exiting at users request...!")
                sys.exit(1)
        return str(VAL)
    
class GetPass():
    """Prompt user to input password on command line. Typed letters will not be displayed"""
    def __init__(self, prompt="Enter Password Here: "):
        self.prompt = prompt

    def prompt_pass(self):
        """Function to prompt password"""
        try:
            pswd = getpass.getpass(self.prompt)
            return pswd
        except Exception as er:
            print(f"Error: {er}")
            return None
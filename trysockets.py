#!/usr/bin/env python3

import socket, re, argparse, threading
from datetime import datetime

class BaseCl():
    def __init__(self):
        parser = argparse.ArgumentParser(description="Mini Network Socket application. Listens on a TCP port and accepts some cmds.")
        parser.add_argument("--port", "-p", type=int, default=9090, help="specify a TCP Port to listen. Default is 9090.")
        parser.add_argument("--log", "-l", type=str, default="/Users/abhat/logs/trysockets.log", help="Specify file to log app output.")
        self.args = parser.parse_args()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.maxconn = 5
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.help_p = re.compile(r'^help$|^\?$', re.I)
        self.hello_p = re.compile(r'^hello$', re.I)
        self.quit_p = re.compile(r'^quit$|^q$|^exit$|^disconnect$|^disconn$', re.I)
        self.date_p = re.compile(r'^date$', re.I)
        self.time_p = re.compile(r'^time$', re.I)

class Getstuff(BaseCl):
    def getdttm(self):
        dttm = datetime.now()
        dt = (str(dttm.year) + "-" + str(dttm.month) + "-" + str(dttm.day)).encode('utf-8')
        tm = (str(dttm.hour) + ":" + str(dttm.minute) + ":" + str(dttm.second)).encode('utf-8')
        return(dt, tm)

class ListenPort(BaseCl):
    def handle_conn(self, con, addrstr, lfl):
        print("Connected to ClientIP: %s" % addrstr)
        gtstuf = Getstuff()
        while True:
            mesg = con.recv(10240).decode('utf-8').rstrip()
            if self.quit_p.search(mesg):
                break
            elif self.help_p.search(mesg):
                print("Help requested from Client - %s" % addrstr)
                lfl.write("Help requested from Client - %s" % addrstr)
                con.send("Commands accepted: 'hello', 'date', 'time', 'help', 'quit'.\n Anything else will be taken as a message.\n".encode('utf-8'))
            elif self.hello_p.search(mesg):
                print("Command from ClientIP - %s: %s" % (addrstr, mesg))
                lfl.write("Command from ClientIP - %s: %s" % (addrstr, mesg))
                con.send("Hello there Buddy!\n".encode('utf-8'))
            elif self.date_p.search(mesg):
                print("Command from ClientIP - %s: %s" % (addrstr, mesg))
                lfl.write("Command from ClientIP - %s: %s" % (addrstr, mesg))
                (DT, TM) = gtstuf.getdttm()
                con.send("DATE: %b\n".encode('utf-8') % DT)
            elif self.time_p.search(mesg):
                print("Command from ClientIP - %s: %s" % (addrstr, mesg))
                lfl.write("Command from ClientIP - %s: %s" % (addrstr, mesg))
                (DT, TM) = gtstuf.getdttm()
                con.send("TIME: %b\n".encode('utf-8') % TM)
            else:
                print("Message from ClientIP - %s: %s" % (addrstr, mesg))
                lfl.write("Message from ClientIP - %s: %s" % (addrstr, mesg))
                con.send("Got your message, Thanks!\n".encode('utf-8'))
        lfl.close()
        con.close()
        print("Connection with Client %s ended!" % addrstr)
        return

    def start_srv(self):
        self.Server.bind((self.HOST, self.args.port))
        self.Server.listen(self.maxconn)
        logfl = open(self.args.log, 'a')
        while True:
            conn, (addr, port) = self.Server.accept()
            thrd = threading.Thread(target=self.handle_conn, args=(conn, str(addr), logfl))
            thrd.start()
            print("Active Connections: %d" % (threading.activeCount() -1))
        return

class MainProg(BaseCl):
    def main(self):
            print("Starting Server connection Listener...")
            lstn = ListenPort()
            lstn.start_srv()
            return


if __name__ == "__main__":
    socketsrv = MainProg()
    socketsrv.main()

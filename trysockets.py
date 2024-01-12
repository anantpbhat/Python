#!/usr/bin/env python3

import socket, re, argparse, threading, concurrent.futures, getstuff, logit

class BaseCl():
    def __init__(self):
        parser = argparse.ArgumentParser(description="Mini Network Socket application. Listens on a TCP port and accepts some cmds.")
        parser.add_argument("--port", "-p", type=int, default=9090, help="specify a TCP Port to listen. Default is 9090.")
        parser.add_argument("--log", "-l", type=str, default="/Users/abhat/logs/trysockets.log", help="Specify file to log app output.")
        self.args = parser.parse_args()
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.maxconn = 5
        self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         ### SOCK_STREAM represents a TCP connection
        self.help_p = re.compile(r'^help$|^\?$', re.I)
        self.hello_p = re.compile(r'^hello$', re.I)
        self.quit_p = re.compile(r'^quit$|^q$|^exit$|^disconnect$|^disconn$', re.I)
        self.date_p = re.compile(r'^date$', re.I)
        self.time_p = re.compile(r'^time$', re.I)

class ListenPort(BaseCl):
    def handle_conn(self, con, addrstr):
        print("Connected to ClientIP: %s" % addrstr)
        logfl = self.args.log
        gtstuf = getstuff.Getstuff()
        log_it = logit.LogIt()
        while True:
            mesg = con.recv(10240).decode('utf-8').rstrip()
            (DT, TM) = gtstuf.getdttm()
            if self.quit_p.search(mesg):
                break
            elif self.help_p.search(mesg):
                log_it.wrtnow("Help requested from Client - %s" % addrstr, logfl)
                con.send("Commands accepted: 'hello', 'date', 'time', 'help', 'quit'.\n Anything else will be taken as a message.\n".encode('utf-8'))
            elif self.hello_p.search(mesg):
                log_it.wrtnow("Command from ClientIP - %s: %s" % (addrstr, mesg), logfl)
                con.send("Hello there Buddy!\n".encode('utf-8'))
            elif self.date_p.search(mesg):
                log_it.wrtnow("Command from ClientIP - %s: %s" % (addrstr, mesg), logfl)
                con.send("DATE: %b\n".encode('utf-8') % DT)
            elif self.time_p.search(mesg):
                log_it.wrtnow("Command from ClientIP - %s: %s" % (addrstr, mesg), logfl)
                con.send("TIME: %b\n".encode('utf-8') % TM)
            else:
                log_it.wrtnow("Message from ClientIP - %s: %s" % (addrstr, mesg), logfl)
                con.send("Got your message, Thanks!\n".encode('utf-8'))
        con.close()
        log_it.wrtnow("Connection with Client %s ended!" % addrstr, logfl)
        return

    def start_srv(self):
        self.Server.bind((self.HOST, self.args.port))
        self.Server.listen(self.maxconn)
        while True:
            conn, (addr, port) = self.Server.accept()
            #exe = concurrent.futures.ThreadPoolExecutor(max_workers=5)
            #exe.submit(self.handle_conn, conn, str(addr))
            thrd = threading.Thread(target=self.handle_conn, args=(conn, str(addr)))
            thrd.start()
            print("Active Connections: %d" % (threading.activeCount() - 1))     ### Active connections not avail in futures module.
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

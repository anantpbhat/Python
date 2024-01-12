
import socket, re, argparse

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
        return

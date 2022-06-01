#!/usr/bin/env python3

import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Server.bind()(HOST, PORT))
Server.listen(5)

while true:
    communication_socket, address = Server.accept()
    print("Connect to IP: %s" % address)
    mesg = communication_socket.recv(1024).decode('utf-8')
    print("Message from Client: %s" % mesg)
    

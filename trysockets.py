#!/usr/bin/env python3

import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

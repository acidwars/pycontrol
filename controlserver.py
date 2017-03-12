#!/usr/bin/env python3.5
import socket
import sys
import argparse
import ssl
import control
import threading

class SSLServer:

    def __init__(self, ip, port, verbosity):
        self.ip = ip
        self.port = port
        self.verbosity = verbosity


    def connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket = ssl.wrap_socket(sock,keyfile='ca.key', certfile='ca.crt', \
            cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1_2, \
            ciphers='ECDH', do_handshake_on_connect=True)
            #ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
            mySocket.bind((self.ip,self.port))
            mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mySocket.listen(2)
            conn, addr = mySocket.accept()
            return(conn, addr)
        except KeyboardInterrupt:
            sys.exit("closing")

    def server(self):
        try:

            conn, addr = SSLServer.connect(self)
            while True:
                data = conn.recv(1024).decode()
                if self.verbosity == 1:
                    print("[~] RECIEVED " + data)
                command = control.ServerCommands(data)
                command = command.commands()
                conn.send(command.encode())
            conn.close()
        except KeyboardInterrupt:
            conn.close()
            sys.exit("closing")
        except BrokenPipeError:
            SSLServer.server(self)

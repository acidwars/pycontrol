#!/usr/bin/env python3.5
import socket
import sys
import argparse
import ssl
import time
from ssl_server import bcolors
import threading

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.add_argument("--ip", help="listening ip")
    parser.add_argument("--port", help="listening port", type=int)
    args = parser.parse_args()
    if args.verbosity:
        print("verbosity turned on")

    try:
        if args.ip:
            host = args.ip
        else:
            host = '127.0.0.1'
        if args.port:
            port = args.port
        else:
            port = 50000

        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2, \
        certfile='client.crt',keyfile='client.key', ciphers='ECDH')
        wrappedSocket.connect((host, port))
        print(bcolors.OKBLUE + repr(wrappedSocket.getpeername()))
        print(wrappedSocket.cipher())
        print(bcolors.ENDC)

        print("connected... ")

        message = input(">>> ")
        while message != "q":
                #mySocket.send(message.encode())
                wrappedSocket.send(message.encode())
                #data = mySocket.recv(1024).decode()
                data = wrappedSocket.recv(1024).decode()
                #data.encode("utf-8")
                print(bcolors.HEADER + data + bcolors.ENDC)
                message = input(">>> ")
        #mySocket.close()
        wrappedSocket.close()
    except KeyboardInterrupt:
        #mySocket.close()
        wrappedSocket.close()
        sys.exit(0)
    except ConnectionRefusedError:
        print(bcolors.FAIL + "connection refused" + bcolors.ENDC)
        time.sleep(5)
        print(bcolors.HEADER +  "reconnecting" + bcolors.ENDC)
        Main()
    except BrokenPipeError:
        print("Broken pipe :(")
        #Main()
    except IndexError:
        print("Please specify a port!")
        print(sys.argv[0] + " PORT")
    except EOFError as e:
        print(e)
        #mySocket.close()
        wrappedSocket.close()
    except ssl.SSLEOFError as e:
        print(e)
        #Main()

if __name__ == '__main__':
    Main()

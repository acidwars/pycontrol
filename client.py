#!/usr/bin/env python3.5
import socket
import sys
import argparse
import ssl
from ssl_server import bcolors

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.add_argument("--ip", help="listening ip")
    parser.add_argument("--port", help="listening port", type=int)
    args = parser.parse_args()
    if args.verbosity:
        print("verbosity turned on")

    try:
        host = args.ip
        port = args.port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2, certfile='client.crt',keyfile='client.key')
        wrappedSocket.connect((host, port))
        print(repr(wrappedSocket.getpeername()))
        print(wrappedSocket.cipher())
        #wrappedSocket.do_handshake
        #mySocket.connect((host,port))

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
    except ConnectionRefusedError:
        print("Can't connect :(")
    except BrokenPipeError:
        print("Broken pipe :(")
    except IndexError:
        print("Please specify a port!")
        print(sys.argv[0] + " PORT")
    except EOFError:
        #mySocket.close()
        wrappedSocket.close()

if __name__ == '__main__':
    Main()

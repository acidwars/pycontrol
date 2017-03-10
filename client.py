#!/usr/bin/env python3.6
import socket
import sys
import argparser

def Main():
    try:
        host = '172.30.96.124'
        port = int(sys.argv[1])
        
        mySocket = socket.socket()
        mySocket.connect((host,port))
        
        print("connected... ")
        message = input(">>> ")
        
        while message != "q":
                mySocket.send(message.encode())
                data = mySocket.recv(1024).decode()
                print("<<< " + data)
                
                message = input(">>> ")
                
        mySocket.close()
    except KeyboardInterrupt:
        mySocket.close()
    except ConnectionRefusedError:
        print("Can't connect :(")
    except BrokenPipeError:
        print("Broken pipe :(")
    except IndexError:
        print("Please specify a port!")
        print(sys.argv[0] + " PORT")
    except EOFError:
        mySocket.close()

if __name__ == '__main__':
    Main()

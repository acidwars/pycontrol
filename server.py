#!/usr/bin/env python3.6
import socket
import subprocess
import sys
import platform
import argparse

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="increase output verbosity")
    parser.add_argument("--ip", help="listening ip")
    parser.add_argument("--port", help="listening port", type=int)
    args = parser.parse_args()
    if args.verbosity:
        print("verbosity turned on")
    while True:
        try:
            host = args.ip
            port = int(args.port)
            mySocket = socket.socket()
            mySocket.bind((host,port))
            mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
            mySocket.listen(1)
            conn, addr = mySocket.accept()
            print ("Connection from: " + str(addr))
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print ("from connected  user: " + str(data))
                test = commands(data)
                if test == None:
                    test = "none"
                conn.send(test.encode())
            
            conn.close()

        except KeyboardInterrupt:
            print("closing...")
            if conn:
                conn.close()
                sys.exit("closing")
            sys.exit("closing")
        except OSError as e:
            print("Port is already in use :(")
            print(e)
            sys.exit("closing")
        except IndexError:
            print("Please specify a port!")
            print(sys.argv[0] + " PORT")
            sys.exit("closing")


def commands(cmd):
    if cmd == "help":
        man = "1. OS\n<<< 2. Uptime\n<<< 3. Kernel\n"
        return man
    if cmd == "1":
        os = platform.linux_distribution()
        return str(os)
    if cmd == "2":
        process = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        return str(process.communicate()[0])
    if cmd == "3":
        kernel = platform.platform()
        return kernel
    else:
        cmd = cmd.split()
        try:
            process = subprocess.Popen([cmd[0], cmd[1]], shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            return str(process.communicate()[0])
        except IndexError:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            return str(process.communicate()[0])

if __name__ == '__main__':
    Main()

#!/usr/bin/env python3.5
import socket
import subprocess
import sys
import platform
import argparse
import shlex
import ssl

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", help="increase output verbosity", type=int)
    parser.add_argument("--ip", help="listening ip")
    parser.add_argument("--port", help="listening port", type=int)
    args = parser.parse_args()
    if args.verbosity:
        print(bcolors.OKBLUE + "verbosity turned on" + bcolors.ENDC)
    while True:
        try:
            if args.ip:
                ip = args.ip
            else:
                ip = '127.0.0.1'
            if args.port:
                port = int(args.port)
            else:
                port = 50000
            if args.verbosity == 1:
                print(bcolors.OKGREEN + " ")
                print("[+] IP: " + ip)
                print("[+] PORT: " + str(port))
                print(bcolors.ENDC)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket = ssl.wrap_socket(sock,keyfile='ca.key', certfile='ca.crt', cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1_2,  do_handshake_on_connect=True)
            ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
            mySocket.bind((ip,port))
            mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mySocket.listen(1)
            conn, addr = mySocket.accept()
            if args.verbosity == 1:
                print (bcolors.WARNING + "Connection from: " + str(addr) + bcolors.ENDC)
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                if args.verbosity == 1:
                    print ("from connected  user: " + str(data))
                test = commands(data)
                if test == None:
                    test = "none"
                conn.send(test.encode())
            conn.close()

        except KeyboardInterrupt:
            try:
                conn.close()
                sys.exit("closing")
            except UnboundLocalError:
                sys.exit("closing")
        except OSError as e:
            if args.verbosity == 1:
                print(bcolors.WARNING)
                print(e)
                print(bcolors.ENDC)
                sys.exit("closing")
        except IndexError:
            if args.verbosity == 1:
                print(bcolors.WARNING)
                print("Please specify a port!")
                print(sys.argv[0] + " PORT")
                print(bcolors.ENDC)
                sys.exit("closing")


def commands(cmd):
    if cmd == "help":
        man = "[+] 1. OS\n[+] 2. Uptime\n[+] 3. Kernel\n[+] 4. show last logins\n"
        return man
    if cmd == "1":
        os = platform.linux_distribution()
        return str(os)
    if cmd == "2":
        process = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
        return str(process.communicate()[0])
    if cmd == "3":
        kernel = platform.platform()
        return str(kernel)
    if cmd == "4":
        process = subprocess.Popen("last", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
        return str(process.communicate()[0])

    else:
        try:
            args = shlex.split(cmd)
            process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, universal_newlines=True)
            return str(process.communicate()[0])
        except IndexError:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            return str(process.communicate()[0])

if __name__ == '__main__':
    Main()

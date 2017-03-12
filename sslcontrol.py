#!/usr/bin/env python3
from controlserver import SSLServer
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity", type=int)
parser.add_argument("--ip", help="listening ip")
parser.add_argument("--port", help="listening port", type=int)
args = parser.parse_args()


def main():
    if args.ip:
        ip = args.ip
    else:
        ip = '127.0.0.1'
    if args.port:
        port = args.port
    else:
        port = 50000
    if args.verbosity:
        verbosity = args.verbosity
    else:
        verbosity = 0
    if verbosity == 1:
        print(bcolors.HEADER + "starting server" + bcolors.ENDC)
        print(bcolors.OKBLUE + "[~] IP:   " + ip + bcolors.ENDC)
        print(bcolors.OKBLUE + "[~] PORT: " + str(port) + bcolors.ENDC)
    server = SSLServer(ip, port, verbosity)
    #server.connect()
    server.server()

if __name__ == '__main__':
    main()

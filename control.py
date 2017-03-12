#!/usr/bin/env python3.5
import platform
import subprocess

class ServerCommands:

    def __init__(self, cmd):
        self.cmd = cmd

    def commands(self):
        if self.cmd == "help":
            man = "\n[+] 1. OS\n[+] 2. Uptime\n[+] 3. Kernel\n[+] 4. show last logins\n[+] 5. show free space\n"
            return man
        if self.cmd == "1":
            os = platform.linux_distribution()
            return str(os)
        if self.cmd == "2":
            process = subprocess.Popen("uptime", shell=True, stdout=subprocess.PIPE,\
            stderr=subprocess.STDOUT, universal_newlines=True)
            return str(process.communicate()[0])
        if self.cmd == "3":
            kernel = platform.platform()
            return str(kernel)
        if self.cmd == "4":
            process = subprocess.Popen("last", shell=True, stdout=subprocess.PIPE,\
            stderr=subprocess.STDOUT, universal_newlines=True)
            return str(process.communicate()[0])
        else:
            failed = "command not found :("
            return (failed)

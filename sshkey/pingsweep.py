#!/usr/bin/python
import os
import socket
import subprocess

CSI = "\x1B["
reset = "{0}m".format(CSI)


class PingSweep(object):
    ##global variables for ping_sweep class
    ip_scan = os.getcwd() + "/ip_scan"
    hostnames = os.getcwd() + "/hostnames"

    def bash(self, command):
        ##Bash method/fuction for execution of Bash commands
        ip_scan_open = open(PingSweep.ip_scan, "w+" + '\n')
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        print CSI + "31;36m" + "{}".format(str(stdout)) + CSI + "0m" + '\n'
        ip_scan_open.write(str(stdout))
        ip_scan_open.close()
        return command

    def ip_2_hostname(self, file_path):
        ##Conversion of ip addresses to hostnames via DNS reverse lookup
        output = open(file_path).readlines()
        hostnames_open = open(PingSweep.hostnames, "w+" + '\n')
        for ip in output:
            try:
                ip_convert = socket.gethostbyaddr(ip.strip())[0]
                hostnames_open.write(ip_convert + '\n')
                print CSI + "31;32m" + "[SUCCESS] {}".format(ip_convert) + CSI + "0m"
            except socket.error as e:
                print CSI + "31;31m" + "[ERROR] {} {}".format(ip, e) + CSI + "0m"
        hostnames_open.close()

    def segment_pull(self):
        ##Entering in network segment and execution of fping -g -a command
        network_enter = CSI + "31;32m" + "Enter network segment x.x.x.x/xx: " + CSI + "0m"
        network = raw_input('{}'.format(network_enter))
        self.bash(["fping", "-g", "-a", network])
        self.ip_2_hostname(PingSweep.ip_scan)


sweep_go = PingSweep()
sweep_go.segment_pull()

#!/usr/bin/python
import os
import sys
import socket
import paramiko
from distutils.util import strtobool
from getpass import getpass

CSI = "\x1B["
reset = "{0}m".format(CSI)


class PubKeyRoller(object):
    ##Global variables for class Pubkey_Roller
    key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
    hosting = socket.gethostname()
    host_file = os.getcwd() + "/hostnames"
    success_host = os.getcwd() + "/success_host"

    def choice_yes_no(self, question):
        ##Bool for yes/no based on user imput
        sys.stdout.write('{}\n'.format(question))
        while True:
            try:
                return strtobool(raw_input())
            except ValueError:
                sys.stdout.write(CSI + "31;31m" + "[ERROR] Enter [y/n]" + CSI + "0m" + '\n')

    def get_hostname(self, file_path):
        ##For loop method parsing hostname file for nodes
        host_data = []

        host_get = open(file_path).readlines()
        for grab_host in host_get:
            host_data.append(grab_host.rstrip())
        return host_data

    def deploy_key(self, key, server, username, password):
        ##Paramiko module for SSH'ing into nodes
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, username=username, password=password)
        client.exec_command('if [ ! -d ~/.ssh ]; then mkdir -p ~/.ssh/; fi')
        if self.outcome == 1:
            client.exec_command("echo '{}' >> ~/.ssh/authorized_keys".format(PubKeyRoller.key))
        elif self.outcome == 0:
            client.exec_command("sed -i '/{}/d' ~/.ssh/authorized_keys".format(PubKeyRoller.hosting))
            client.exec_command("sed -i 's/^[ \t]*//' ~/.ssh/authorized_keys")
            client.exec_command("sed -i 's/[ \t]*$//' ~/.ssh/authorized_keys")
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')

    def key_push(self):
        ##key_push method which calls other methods for the script to work
        user_enter = CSI + "31;32m" + "Enter user: " + CSI + "0m"
        username = raw_input('%s' % user_enter)
        password = getpass(CSI + "31;32m" + "Password:" + CSI + "0m")
        self.outcome = self.choice_yes_no(CSI + "31;36m" + "[y] copy key or [n] delete key" + CSI + "0m")
        host_list = self.get_hostname(PubKeyRoller.host_file)
        host_connect = open(PubKeyRoller.success_host, "w+" + '\n')
        for host in host_list:
            try:
                self.deploy_key(PubKeyRoller.key, host, username, password)
                print CSI + "31;36m" + "Hostname: {}".format(host) + CSI + "0m"
                host_connect.write(host + '\n')
            except paramiko.SSHException as e:
                print CSI + "31;31m" + "{}".format(host) + CSI + "0m"
                print CSI + "31;31m" + "[ERROR] {}".format(e) + CSI + "0m"
            except socket.error as e:
                print CSI + "31;31m" + "{}".format(host) + CSI + "0m"
                print CSI + "31;31m" + "[ERROR] {}".format(e) + CSI + "0m"
        host_connect.close()


key_go = PubKeyRoller()
key_go.key_push()

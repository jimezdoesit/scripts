#!/usr/bin/python
import os
import re
import sys
import socket
import paramiko
from distutils.util import strtobool
from getpass import getpass
from itertools import chain
CSI="\x1B["
reset=CSI+"m"

def choice_yes_no(question):
    sys.stdout.write('{} [y/n]\n' .format(question))
    while True:
       try:
          #return strtobool(raw_input().lower())
          return strtobool(raw_input())
       except ValueError:
          sys.stdout.write(CSI+"31;31m"+"[ERROR] Enter [y/n]"+CSI+"0m"+'\n') 

def get_ip_addresses(file_path):
    ippattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    ip_data = []

    output =  open(file_path).readlines()
    for ip_grab in output:
       findip = re.findall(ippattern,ip_grab)
       ip_data.append(findip) 
    ##list of list will be flatten out by use of itertools :-)
    return list(chain(*ip_data)) 

def deploy_key(key, server, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=username, password=password)
    client.exec_command('if [ ! -d ~/.ssh ]; then mkdir -p ~/.ssh/; fi')
    if outcome == 1:
       client.exec_command("echo '{}' >> ~/.ssh/authorized_keys" .format(key))
    elif outcome == 0:
       client.exec_command("sed -i '/{}/d' ~/.ssh/authorized_keys" .format(hoster))
       client.exec_command("sed -i 's/^[ \t]*//' ~/.ssh/authorized_keys")
       client.exec_command("sed -i 's/[ \t]*$//' ~/.ssh/authorized_keys")
    client.exec_command('chmod 644 ~/.ssh/authorized_keys')
    client.exec_command('chmod 700 ~/.ssh/')

key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
user_enter = CSI+"31;32m" + "Enter user: " + CSI + "0m"
username = raw_input('%s'%user_enter)
hoster = socket.gethostname()
password = getpass(CSI+"31;32m"+"Password"+CSI+"0m") 
outcome = choice_yes_no(CSI+"31;32m"+"[y] copy key or [n] delete key"+CSI+"0m")
host_file = os.getcwd()+"/ipscan"
hosts = get_ip_addresses(host_file)#[0] 
for host in hosts:
    deploy_key(key,host,username,password)
    print CSI+"31;36m"+"Hostname: {}".format(hosts)+CSI+"0m"

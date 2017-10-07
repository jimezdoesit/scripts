#! /usr/bin/python

import subprocess
import os

CSI="\x1B["
reset=CSI+"m"

##Class PSSH script runs & controls tool
class Pssh_Passwd(object):

   ##Global variables
   log = os.getcwd()+"/logfile" 
   home_dir = os.path.expanduser('~/.ssh/config')
   config_set = "Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile /dev/null\n"
   user = [] 
   cmd = []

   def __init__(self):
       ##Raw_input for login user & Bash command
       print CSI+"31;31m" + "[WARNING] This script will alter/delete %s!" % Pssh_Passwd.home_dir+ CSI + "0m"
       print CSI+"31;36m" + "Enter username & bash command?" + CSI + "0m"
       self.user_enter = CSI+"31;36m" + "Enter user: " + CSI + "0m"
       self.user_final = raw_input('%s'%self.user_enter)
       self.cmd_enter = CSI+"31;36m" + "Enter bash command: " + CSI + "0m"
       self.cmd_final = raw_input('%s'%self.cmd_enter)       
       Pssh_Passwd.user.append(self.user_final)
       Pssh_Passwd.cmd.append(self.cmd_final) 

   def config_insert(self):
       ##Scanning for config file & creation of it if needed!
       self.logfile = open(Pssh_Passwd.log,"w+"+'\n')
       if os.path.isfile(Pssh_Passwd.home_dir):
         print CSI+"31;36m" + "Moving existinng %s file & creating new config file." % Pssh_Passwd.home_dir + CSI + "0m"
         self.logfile.write("Moving existinng %s file & creating new config file."  % Pssh_Passwd.home_dir)
         os.rename(Pssh_Passwd.home_dir,Pssh_Passwd.home_dir+".bak")
         self.configfile = open(Pssh_Passwd.home_dir,"w+"+'\n')
         self.configfile.write(Pssh_Passwd.config_set)
         self.configfile.close()
         os.chmod(Pssh_Passwd.home_dir,0600) 
       else:
         print CSI+"31;36m" + "Creating new config %s file." % Pssh_Passwd.home_dir + CSI + "0m"
         self.logfile.write("Creating new config %s file.\n"  % Pssh_Passwd.home_dir)
         self.configfile = open(Pssh_Passwd.home_dir,"w+"+'\n')
         self.configfile.write(Pssh_Passwd.config_set)
         self.configfile.close() 
         os.chmod(Pssh_Passwd.home_dir,0600)   
       self.logfile.close()

   def bash_pssh(self):
       ##Bash PSSH command execution for username & Bash command
       self.logfile = open(Pssh_Passwd.log,"a+"+'\n')
       self.command = ['pssh','-i','-t','0','-h','iplist','-e','log','-l',str(Pssh_Passwd.user[0]),"-A",str(Pssh_Passwd.cmd[0])] 
       self.process = subprocess.Popen(self.command,stdout=subprocess.PIPE)
       self.stdout = self.process.communicate()[0]
       self.pssh_code = str(self.process.returncode)
       if self.process.returncode == 0:
         print CSI+"31;32m" + "[SUCCESSFUL] %s" % self.stdout + CSI + "0m"+'\n'
         self.logfile.write(CSI+"31;32m" + "[SUCCESSFUL] %s\n%s" % (self.stdout,self.pssh_code) + CSI + "0m"+'\n')
       if self.process.returncode == 4:
         print CSI+"31;31m" + "[FAILURE] %s" % self.stdout + CSI + "0m"+'\n'
         self.logfile.write(CSI+"31;31m" + "[FAILURE] %s\n%s" % (self.stdout,self.pssh_code) + CSI + "0m"+'\n')
       if self.process.returncode == 5:
         print CSI+"31;31m" + "[FAILURE] %s" % self.stdout + CSI + "0m"+'\n'
         self.logfile.write(CSI+"31;31m" + "[FAILURE] %s\n%s" % (self.stdout,self.pssh_code) + CSI + "0m"+'\n')
       self.logfile.close()

   def config_remove(self):
       ##Removal of config from home directory!
       self.logfile = open(Pssh_Passwd.log,"a+"+'\n')
       if os.path.exists(Pssh_Passwd.home_dir):
         print CSI+"31;36m" + "Removing %s file." % Pssh_Passwd.home_dir + CSI + "0m"
         self.logfile.write("Removing %s file." % Pssh_Passwd.home_dir+'\n')
         os.remove(Pssh_Passwd.home_dir)
       else:
         print CSI+"31;31m" + "[ERROR] %s file does not exist." % Pssh_Passwd.home_dir + CSI + "0m"
         self.logfile.write("[ERROR] %s file does not exist.." % Pssh_Passwd.home_dir+'\n')
       self.logfile.close()

##Below commands that will run PSSH tool!
go = Pssh_Passwd()
go.config_insert() 
go.bash_pssh()
go.config_remove() 

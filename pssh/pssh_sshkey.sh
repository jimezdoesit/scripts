#! /bin/bash

file="${HOME}/.ssh/config"
username=$(whoami)
config_set="Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile /dev/null"

function coloredEcho(){
    local exp=$1;
    local color=$2;
    if ! [[ ${color} =~ '^[0-9]$' ]] ; then
       case $(echo ${color} | tr '[:upper:]' '[:lower:]') in
        black) color=0 ;;
        red) color=1 ;;
        green) color=2 ;;
        yellow) color=3 ;;
        blue) color=4 ;;
        magenta) color=5 ;;
        cyan) color=6 ;;
        white|*) color=7 ;; # white or invalid color
       esac
    fi
    tput setaf ${color};
    echo ${exp};
    tput sgr0;
}

coloredEcho "[WARNING] This script will delete ~/.ssh/config. Back it up!" red
coloredEcho "This script will attempt to backup any existing ~/.ssh/config file." cyan
read -p "Enter user: " user
read -p "Enter command: " cmd_exec
read -n1 -p "[y] for logging/terminal [n] for terminal: " logging && echo -e "\n"

if [ -e "${file}" ]; then
  #coloredEcho "Moving ${file} file & re-creating ${file}" cyan
  mv -f ${file} ${file}.bak > /dev/null 2>&1
  touch ${file}
  echo -e ${config_set} > ${file}
  chmod -f 0600 ${file}
else
  #coloredEcho "${file} file is not there. Creating ${file}" cyan
  touch ${file}
  echo -e ${config_set} > ${file}
  chmod -f 0600 ${file}
fi

if [ ! -e "logfile" ]; then
  touch logfile
fi

case ${logging} in
   y|Y) pssh -i -t 0 -h hostnames -e log -l ${user} "${cmd_exec}" 2>&1 | tee logfile ;;
   n|N) pssh -i -t 0 -h hostnames -e log -l ${user} "${cmd_exec}" ;;
     *) rm -f ${file} > /dev/null 2>&1 && coloredEcho "[ERROR] y/n for logging?" red && exit 0 ;;
esac

if [ -e "${file}" ]; then
  #coloredEcho "Deleting ${file} file" cyan
  rm -f ${file} > /dev/null 2>&1
fi


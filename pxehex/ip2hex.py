#! /usr/bin/python
import binascii
import optparse
import shutil
import socket
import sys

CSI = "\x1B["
reset = "{0}m".format(CSI)


class Ip2Hex(object):
    ##Global variables for class Ip2Hex
    ipaddress = []
    system = []

    def __init__(self):
        ##Option Parser for passing flags/args into script
        self.parser = optparse.OptionParser(description='IP 2 hex conversion script')
        self.parser.add_option('-a', '--address',
                               action="store_true", dest="ipaddress",
                               help="x.x.x.x", default="flunk")
        self.parser.add_option('-d', '--distro',
                               action="store_true", dest="system",
                               help="distro_file", )
        options, args = self.parser.parse_args()
        if options.ipaddress == "flunk":
            sys.exit(CSI + "31;31m" + "[ERROR] Usage: ./ip2hex.py (-a) x.x.x.x (-d) pxe_ks" + CSI + "0m" + '\n')
        elif not args:
            sys.exit(CSI + "31;31m" + "[ERROR] Usage: ./ip2hex.py (-a) x.x.x.x (-d) pxe_ks" + CSI + "0m" + '\n')
        elif options.ipaddress and not options.system:
            sys.exit(CSI + "31;31m" + "[ERROR] Usage: ./ip2hex.py (-a) x.x.x.x (-d) pxe_ks" + CSI + "0m" + '\n')
        elif len(args) != 2:
            sys.exit(CSI + "31;31m" + "[ERROR] Usage: ./ip2hex.py (-a) x.x.x.x (-d) pxe_ks" + CSI + "0m" + '\n')
        elif options.ipaddress and options.system:
            Ip2Hex.ipaddress.append(args[0])
            Ip2Hex.system.append(args[1])

    def make_hex(self):
        # Hex & ascii conversion of IP address
        hexout = binascii.hexlify(socket.inet_aton(Ip2Hex.ipaddress[0])).upper()
        # source path for hex files
        hexpath = "/x/tftpboot/pxelinux.cfg/"

        # Distro hash table of hex files
        hexfile = {
            'cent72_server': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/cent72_server_hex",
            'cent73_server': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/cent73_server_hex",
            'ubuntu14_server': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/ubuntu14_server_hex",
            'ubuntu14_desktop': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/ubuntu14_desktop_hex",
            'ubuntu16_server': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/ubuntu16_server_hex",
	    'ubuntu16_desktop': "/x/tftpboot/pxelinux.cfg/bin/pxe_ks_files/ubuntu16_desktop_hex",
        }

        # process creates hex file & puts ip address in hex file.
        shutil.copyfile(hexfile[Ip2Hex.system[0]], hexpath + "/" + hexout)
        hexinsert = open(hexpath + "/" + hexout, "a+" + '\n')
        hexinsert.write("#" + Ip2Hex.ipaddress[0] + '\n')
        hexinsert.close()


go = Ip2Hex()
go.make_hex()

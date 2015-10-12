import re
import socket
import os.path
import sys
from pprint import pprint as pp


reverse_map = {}

filename = '/Users/christopher/Code/czdap-tools/zonedata-download/zonefiles/993.txt'


f = open(filename,'r')
regex = re.compile('(\S+)\.\s+(\d+)\s+in\s+ns\s+(\S*)')
for line in f:
    zone = regex.match(line)
    if zone:
        # print zone.group(0)

        print zone.group(1) + " -- " + zone.group(2) + " -- " + zone.group(3)
        try:
            query_result = socket.getaddrinfo(zone.group(1),'80')
            for result in query_result:
                ip = result[4][0]
                print ip
            # pp(query_result)
        except socket.gaierror:
            print zone.group(1) + " NOT FOUND"


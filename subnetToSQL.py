import re
import os.path
import sys
from netaddr import *
from pprint import pprint as pp


reverse_map = {}

filename = '/Users/christopher/Code/domainThing/subnet.csv'

f = open(filename,'r')
regex = re.compile('\"(\d+\.\d+\.\d+\.\d+)\"\,(\d+)')
for line in f:
    matched = regex.match(line)
    if matched:
        subnet = IPNetwork(matched.group(1) + "/" + matched.group(2))
        for ip in subnet:
            print '%s' % ip

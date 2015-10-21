import re
import os.path
import sys
from netaddr import *
from pprint import pprint as pp
import mysql.connector
from datetime import datetime

filename = '/Users/christopher/Code/domainThing/subnet.csv'


config = {
  'user': 'domains',
  'password': 'ThisistheDomains)(',
  'host': '173.193.23.40',
  'database': 'domainThing',
  'raise_on_warnings': True,
}

sql = mysql.connector.connect(**config)
cursor = sql.cursor()

add_ip = ("INSERT INTO ip_address "
               "(ip) "
               "VALUES (%s)")



### TODO make inserts larger
time = datetime.now()
print time.strftime("%Y-%m-%d %H:%M:%S.%f")
f = open(filename,'r')
regex = re.compile('\"(\d+\.\d+\.\d+\.\d+)\"\,(\d+)')
for line in f:
    matched = regex.match(line)
    time = datetime.now()
    if matched:
        subnet = IPNetwork(matched.group(1) + "/" + matched.group(2))
        
        if subnet[0].is_private():
            print str(subnet) + " IS PRIVATE!"
            continue
        print subnet
        ip_array = []
        ip_count = 0
        for ip in subnet:

            # print '%s' % ip.value
            ip_number = [ip.value]
            ip_array.append(ip_number)
            ip_count = ip_count + 1
            if ip_count > 1000:
                print "INSERTING 1000 records"
                cursor.executemany(add_ip,ip_array)
                sql.commit()  
                ip_count = 0
                ip_array = []

        print "INSERTING %s records" % ip_count
        print time.strftime("%Y-%m-%d %H:%M:%S.%f")
        # pp(ip_array)
        cursor.executemany(add_ip,ip_array)
        sql.commit()


cursor.close()
sql.close()





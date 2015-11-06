import re
import os.path
import sys
from netaddr import *
from pprint import pprint as pp
import mysql.connector
from datetime import datetime
import configparser as ConfigParser

"""
This script is pretty lazy, and will just add ips all day.
Uses mysql at the end to actually make sure each record is only 
in the db once.
"""

class subnetToSql():

    def __init__(self):

        configFile = './config.cfg'
        config = ConfigParser.ConfigParser()
        config.read(configFile)

        my_config = {
          'user': config.get('mysql','user'),
          'password': config.get('mysql','password'),
          'host': config.get('mysql','host'),
          'database': config.get('mysql','database')
        }

        self.subnetFile = config.get('subnetToSql','file')
        self.sql = mysql.connector.connect(**my_config)
        self.cursor = self.sql.cursor()
        add_ip = ("INSERT INTO ip_address (ip) VALUES (%s)")

    def __exit__(self):
        self.cursor.close()
        self.sql.close()

    def main(self):
        time = datetime.now()
        print time.strftime("%Y-%m-%d %H:%M:%S.%f")
        f = open(self.subnetFile,'r')
        regex = re.compile('\"(\d+\.\d+\.\d+\.\d+)\"\,(\d+)')
        for line in f:
            matched = regex.match(line)
            time = datetime.now()
            if matched:
                subnet = IPNetwork(matched.group(1) + "/" + matched.group(2))
                if subnet[0].is_private():
                    print("Skipping private subnet")
                    continue
                ip_array = []
                ip_count = 0
                for ip in subnet:
                    # print '%s' % ip.value
                    ip_number = [ip.value]
                    ip_array.append(ip_number)
                    ip_count = ip_count + 1
                    if ip_count > 1000:
                        print "INSERTING 1000 records"
                        self.cursor.executemany(add_ip,ip_array)
                        self.sql.commit()  
                        ip_count = 0
                        ip_array = []
                print "INSERTING %s records" % ip_count
                print time.strftime("%Y-%m-%d %H:%M:%S.%f")
                # pp(ip_array)
                self.cursor.executemany(add_ip,ip_array)
                self.sql.commit()

    def dedupe(self):
        print("RUNNING: INSERT INTO ip_address_unique (ip) select distinct(ip) from ip_address;")
        make_unique = "INSERT INTO ip_address_unique (ip) select distinct(ip) from ip_address;"
        self.cursor.execute(make_unique)
        self.sql.commit()


if __name__ == "__main__":
    main = subnetToSql()
    main.main()
    main.dedupe()




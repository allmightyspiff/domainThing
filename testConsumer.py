#!/usr/bin/env python
import mysql.connector
import json
from netaddr import *
from pprint import pprint as pp
from datetime import datetime, timedelta

config = {
  'user': 'domains',
  'password': 'ThisistheDomains)(',
  'host': '173.193.23.40',
  'database': 'domainThing',
  'raise_on_warnings': True,
}

sql = mysql.connector.connect(**config)
cursor = sql.cursor()
query = ("SELECT ip from ip_address_unique WHERE ip = %(int_ip)s LIMIT 1 ")

print ' [*] Waiting for messages. To exit press CTRL+C'

domains = [
    {'ip': '75.126.132.188', 'domain':'test1.com'}, 
    {'ip':'158.85.89.244', 'domain':'test2.com'}
    ]


final_domain = []
# print " [x] Received %r" % (body,)
for domain in domains:
    if domain['ip'] == "UNRESOLVEABLE":
        nownow = datetime.now()
        domain['lookupTime'] = 0
        domain['finalStartTime'] = nownow.isoformat()
        domain['softlayer'] = 0
        continue

    start = datetime.now()
    try:
        ip = IPAddress(domain['ip'])
    except:
        ip = IPAddress('0.0.0.0')
    
    cursor.execute(query,{ 'int_ip' : ip.value})
    results = cursor.fetchall()
    print cursor.statement
    pp(results)

    print domain['domain'] + " => " + domain['ip'] + " - " + str(ip.value)
    nownow = datetime.now()
    elapsed = nownow - start
    domain['lookupTime'] = elapsed.total_seconds()
    domain['finalStartTime'] = nownow.isoformat()
    if cursor.rowcount > 0:
        print str(cursor.rowcount) + " Rows Found"
        domain['softlayer'] = 1
    else:
        domain['softlayer'] = 0

    pp(domain)
    # Going through the cursor is required for some reason
    # Need to just remove this i think


print("Jobs done")
# pp(domains)



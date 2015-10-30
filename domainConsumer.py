#!/usr/bin/env python
import pika
import mysql.connector
import json
from netaddr import *
from pprint import pprint as pp
from datetime import datetime, timedelta
import elasticsearch


credentials = pika.PlainCredentials('domainThing', 'thisDomainThingy')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               '173.193.23.40',
               5672,
               '/',
               credentials)
            )

channel = connection.channel()
channel.queue_declare(queue='domains')
config = {
  'user': 'domains',
  'password': 'ThisistheDomains)(',
  'host': '173.193.23.40',
  'database': 'domainThing',
  'raise_on_warnings': True,
}

es = elasticsearch.Elasticsearch([{'host':'10.37.82.159'}])  

sql = mysql.connector.connect(**config)
cursor = sql.cursor()
query = ("SELECT ip from ip_address_unique WHERE ip = %(int_ip)s LIMIT 1")

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    domains = json.loads(body)
    final_domain = []
    for domain in domains:

        start = datetime.now()
        try:
            ip = IPAddress(domain['ip'])
        except:
            ip = IPAddress('0.0.0.0')

        cursor.execute(query,{ 'int_ip' : ip.value})
        # Need to fetch the results or else an exception gets thrown
        results = cursor.fetchall()
        print domain['domain'] + " => " + domain['ip'] + " - " + str(ip.value)
        nownow = datetime.now()
        elapsed = nownow - start
        domain['lookupTime'] = elapsed.total_seconds()
        domain['finalStartTime'] = nownow.isoformat()
        if cursor.rowcount > 0:
            domain['softlayer'] = 1
        else:
            domain['softlayer'] = 0

        es.index(index="domain-final",doc_type="blog",body=json.dumps(domain))

    print("Jobs done")
    # pp(domains)
    ch.basic_ack(delivery_tag = method.delivery_tag)



channel.basic_consume(callback,queue='domains')
channel.start_consuming()

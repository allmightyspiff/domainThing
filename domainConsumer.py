#!/usr/bin/env python
import pika
import mysql.connector
import json
from netaddr import *
from pprint import pprint as pp
from datetime import datetime, timedelta
import elasticsearch
import configparser 

class domainConsumer():

    def main(self):
        configFile = './config.cfg'
        config = configparser.ConfigParser()
        config.read(configFile)
        credentials = pika.PlainCredentials(
                    config.get('rabbitmq','user'), 
                    config.get('rabbitmq','password')
                )
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                    config.get('rabbitmq','host'), 
                    config.getint('rabbitmq','port'), 
                    config.get('rabbitmq','vhost'), 
                    credentials, 
                    socket_timeout=15)
                )

        channel = connection.channel()
        channel.queue_declare(queue='domains')
        my_config = {
          'user': config.get('mysql','user'),
          'password': config.get('mysql','password'),
          'host': config.get('mysql','host'),
          'database': config.get('mysql','database')
        }

        es = elasticsearch.Elasticsearch([{'host':config.get('elasticsearch','host')}])  

        sql = mysql.connector.connect(**my_config)
        cursor = sql.cursor()
        query = ("SELECT ip from ip_address_unique WHERE ip = %(int_ip)s LIMIT 1")
        channel.basic_consume(self.callback,queue='domains')
        channel.start_consuming()

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
            logger.info("%s, %s, %s"  % (domain['domain'], domain['ip'], str(ip.value)))

            nownow = datetime.now()
            elapsed = nownow - start
            domain['lookupTime'] = elapsed.total_seconds()
            domain['finalStartTime'] = nownow.isoformat()
            if cursor.rowcount > 0:
                domain['softlayer'] = 1
            else:
                domain['softlayer'] = 0

            es.index(index="domain-final",doc_type="blog",body=json.dumps(domain))

        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == "__main__":
    logger.basicConfig(filename="parser.log", format='%(asctime)s, %(message)s' ,level=logger.INFO)
    try:
        consumer = domainConsumer()
        consumer.main()
    except BaseException as e:
        logger.exception(str(e))



#!/usr/bin/env python
import pika
import mysql.connector
import json
from netaddr import *
from pprint import pprint as pp
from datetime import datetime, timedelta
import elasticsearch
import configparser 
import logging as logger
import time
from multiprocessing import Process, current_process, active_children

class domainConsumer():

    def __init__(self,indexName="domain-final"):
        logger.getLogger("elasticsearch").setLevel(logger.WARNING)
        configFile = './config.cfg'
        config = configparser.ConfigParser()
        config.read(configFile)

        pika_cred = pika.PlainCredentials(
                        config.get('rabbitmq','user'), 
                        config.get('rabbitmq','password')
                    )
        pika_param = pika.ConnectionParameters(
                        config.get('rabbitmq','host'), 
                        config.getint('rabbitmq','port'), 
                        config.get('rabbitmq','vhost'), 
                        credentials=pika_cred,
                        heartbeat_interval=500,
                        connection_attempts=3,
                        socket_timeout=15
                    )
        self.pika_conn =  pika.BlockingConnection(pika_param)
        self.channel = self.pika_conn.channel()

        my_config = {
          'user': config.get('mysql','user'),
          'password': config.get('mysql','password'),
          'host': config.get('mysql','host'),
          'database': config.get('mysql','database')
        }

        self.es = elasticsearch.Elasticsearch([{'host':config.get('elasticsearch','host')}])  

        self.sql = mysql.connector.connect(**my_config)
        self.cursor = self.sql.cursor()
        self.query = ("SELECT ip from ip_address_unique WHERE ip = %(int_ip)s LIMIT 1")
        self.doStats = 0
        self.index = indexName
        self.doStats = 0
        self.stats = {
            'domains' : 0,
            'startTime' : 0,
            'endTime' : 0,
            'runningSeconds': 0,
            'avg': []
        }

    def gogo(self, pid):
        
        while True:
            logger.info("Staring to CONSUME %s" , pid)
            try:
                self.main()
            except BaseException as e:
                logger.exception(str(e))
            logger.info("There was an error CONSUMING. Sleeping for 600")
            time.sleep(600)

    def main(self):
        
        self.channel.queue_declare(queue='domains')

        self.channel.basic_consume(self.callback,queue='domains')
        self.channel.start_consuming()

    def singleRun(self):
        self.doStats = 1
        start = datetime.now()
        self.stats['startTime'] = start
        self.channel.queue_declare(queue='domains')
        self.channel.basic_consume(self.callback,queue='domains')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.pika_conn.close()
        logger.info("Start: %s" % (self.stats['startTime']))
        logger.info("Ddomains: %s" % (self.stats['domains']))
        logger.info("runningSeconds: %s" % (self.stats['runningSeconds']))
        logger.info("Average domains/s %s" % (self.stats['avg']))
        logger.info("End: %s" % (self.stats['endTime']))

    def callback(self, ch, method, properties, body):
        domains = json.loads(body)
        final_domain = []
        main_start = datetime.now()
        for domain in domains:

            start = datetime.now()
            try:
                ip = IPAddress(domain['ip'])
            except:
                ip = IPAddress('0.0.0.0')

            self.cursor.execute(self.query,{ 'int_ip' : ip.value})
            # Need to fetch the results or else an exception gets thrown
            results = self.cursor.fetchall()
            # logger.info("%s, %s, %s"  % (domain['domain'], domain['ip'], str(ip.value)))

            nownow = datetime.now()
            elapsed = nownow - start
            domain['lookupTime'] = elapsed.total_seconds()
            domain['finalStartTime'] = nownow.isoformat()
            if self.cursor.rowcount > 0:
                domain['softlayer'] = 1
            else:
                domain['softlayer'] = 0

            self.es.index(index=self.index,doc_type="blog",body=json.dumps(domain))

        ch.basic_ack(delivery_tag = method.delivery_tag)
        main_end = datetime.now()
        elapsed = main_end - main_start
        domain_count = len(domains)
        elapsed = nownow - start
        if (elapsed.total_seconds() > 0):
            ds = round(domain_count / elapsed.total_seconds())
        else:
            ds = 0
   
        logger.info("consumed %s domains in %ss" % (domain_count, elapsed, ds))
        if self.doStats:
            self.stats['domains'] = self.stats['domains'] + domain_count
            self.stats['endTime'] = datetime.now().isoformat()
            self.stats['runningSeconds'] =self.stats['runningSeconds'] + elapsed
            self.stats['avg'].append(ds)

if __name__ == "__main__":
    logger.basicConfig(filename="consumer-%d.log" % pid, format='%(asctime)s, %(message)s' ,level=logger.INFO)
    configFile = './config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    maxProcs = config.getint('domainConsumer','processes')
    for x in range(maxProcs):
        consumer = domainConsumer()
        Process(target=consumer.gogo,args=(x,)).start()





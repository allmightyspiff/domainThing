#!/usr/bin/env python
import pika
import mysql.connector
import json
from netaddr import *
from pprint import pprint as pp
from datetime import datetime, timedelta
import elasticsearch
import configparser 
import logging
import time
from multiprocessing import Process, current_process, active_children
from mqlightQueue import mqlightQueue

class domainConsumer():

    def __init__(self,indexName="domain-final"):
        configFile = './config.cfg'
        config = configparser.ConfigParser()
        config.read(configFile)
        self.packetSize = config.getint('domainParser','packetSize')
        clientName = 'consumer_000' 
        self.q = mqlightQueue(config,clientName)
        while not self.q.ready:
            logging.info("Consumer: Not ready yet")
            time.sleep(1)

        my_config = {
          'user': config.get('mysql','user'),
          'password': config.get('mysql','password'),
          'host': config.get('mysql','host'),
          'database': config.get('mysql','database')
        }

        self.es = elasticsearch.Elasticsearch([{'host':config.get('elasticsearch','host')}])  
        es_log = logging.getLogger("elasticsearch")
        es_log.setLevel(logging.CRITICAL)
        es_log.disabled=True
        logging.getLogger("elasticsearch.trace").setLevel(logging.CRITICAL)

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
            logging.info("Staring to CONSUME %s" , pid)
            try:
                self.main()
            except BaseException as e:
                logging.exception(str(e))
            logging.info("There was an error CONSUMING. Sleeping for 600")
            time.sleep(600)

    def main(self):
        return True
        # self.channel.queue_declare(queue='domains')

        # self.channel.basic_consume(self.callback,queue='domains')
        # self.channel.start_consuming()

    # def singleRun(self):
    #     self.doStats = 1
    #     start = datetime.now()
    #     self.stats['startTime'] = start
    #     self.channel.queue_declare(queue='domains')
    #     self.channel.basic_consume(self.callback,queue='domains')
    #     try:
    #         self.channel.start_consuming()
    #     except KeyboardInterrupt:
    #         self.channel.stop_consuming()
    #     except IOError:
    #         self.channel.stop_consuming()
    #     self.pika_conn.close()
    #     self.printStats()

    def mqRun(self):
        self.doStats = 1
        start = datetime.now()
        self.stats['startTime'] = start
        try:
            self.q.subscribe('domains',self.callbackMQL)
        except BaseException as e:
            pp(e)
            # self.q.unsubscribe('domains')
            self.q.close()
            exit(0)

    def consumeDomains(self,domains):
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
            # logging.info("%s, %s, %s"  % (domain['domain'], domain['ip'], str(ip.value)))

            nownow = datetime.now()
            elapsed = nownow - start
            domain['lookupTime'] = elapsed.total_seconds()
            domain['finalStartTime'] = nownow.isoformat()
            if self.cursor.rowcount > 0:
                domain['softlayer'] = 1
            else:
                domain['softlayer'] = 0

            self.es.index(index=self.index,doc_type="blog",body=json.dumps(domain))
        logging.info("CONSUMED %s domains" % len(domains))



    def callbackMQL(self, message_type, data, delivery):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>CALLBACKMQL")
        start = datetime.now()
        domains = json.loads(data)
        logging.info("Got %s domains" % len(domains))
        message = self.consumeDomains(domains)
        delivery['message']['confirm_delivery']()
        nownow = datetime.now()

        if self.doStats:
            self.updateStats(start, len(domains), nownow)

        if len(domains) < self.packetSize:
            self.printStats()
            self.q.ready = False 
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<CALLBACKMQL")


    def callback(self, ch, method, properties, body):
        start = datetime.now()
        domains = json.loads(body)
        self.consumeDomains(domains)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        nownow = datetime.now()

        if self.doStats:
            self.updateStats(start, len(domains), nownow)

        if domain_count < self.packetSize:
            raise IOError


    def updateStats(self, startTime, domainCount, endTime):
        elapsed = endTime - startTime
        if (elapsed.total_seconds() > 0):
            ds = round(domainCount / elapsed.total_seconds())
        else:
            ds = 0
        logging.info("resolved %s domains in %ss - %s d/s" % (domainCount, elapsed.total_seconds(), ds ))
        self.stats['domains'] = self.stats['domains'] + domainCount
        self.stats['runningSeconds'] =self.stats['runningSeconds'] + elapsed.total_seconds()
        self.stats['avg'].append(ds)
        self.stats['endTime'] = endTime.isoformat()

    def printStats(self):
        logging.info("Start: %s" % (self.stats['startTime']))
        logging.info("Domains: %s" % (self.stats['domains']))
        logging.info("runningSeconds: %s" % (self.stats['runningSeconds']))
        logging.info("Average domains/s %s" % (self.stats['avg']))
        logging.info("End: %s" % (self.stats['endTime']))


if __name__ == "__main__":
    logging.basicConfig(filename="consumer-%d.log" % pid, format='%(asctime)s, %(message)s' ,level=logging.INFO)
    configFile = './config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    maxProcs = config.getint('domainConsumer','processes')
    for x in range(maxProcs):
        consumer = domainConsumer()
        Process(target=consumer.gogo,args=(x,)).start()





#!/usr/bin/env python
import pika
import json
import socket
from datetime import datetime, timedelta
from pprint import pprint as pp
import time
import logging as logger
from multiprocessing import Process, current_process, active_children
import Queue
import threading
import configparser
from mqlightQueue import mqlightQueue


class domainThread(threading.Thread):

    def __init__(self, domain, queue, threadId):
        threading.Thread.__init__(self)
        self.domain = domain
        self.queue = queue
        self.threadId = threadId
        self.fqdn = socket.getfqdn()

    def run(self):
        self.processDomain(self.domain,self.queue)

    def getZoneIp(self,zone):
        ip = None
        try:
            query_result = socket.getaddrinfo(zone,'80')
            for result in query_result:
                ip = result[4][0]

        except socket.gaierror:
            return ip
            # print zone + " NOT FOUND"
        except:
            # something went WILDLY wrong
            return ip
        return ip

    def processDomain(self,domain, workQueue):
        start = datetime.now()
        thisZone = domain['domain']
        
        zoneIp = self.getZoneIp(thisZone)
        if zoneIp is None:
            zoneIp = self.getZoneIp("www." + thisZone)
            domain['domain'] = "www." + thisZone
        if zoneIp is None:
            zoneIp = "UNRESOLVEABLE"

        nownow = datetime.now()
        elapsed = nownow - start
        domain['ip'] = zoneIp
        domain['resolveTime'] = elapsed.total_seconds()
        domain['ipCreateTime'] = nownow.isoformat()
        domain['resolverHost'] = self.fqdn
        # logger.info("%s - %s - %s" % ( thisZone, zoneIp, self.threadId))
        workQueue.put(domain)
        return True

class domainResolver():
    def __init__(self):
        configFile = './config.cfg'
        config = configparser.ConfigParser()
        config.read(configFile)

        self.packetSize = config.getint('domainParser','packetSize')

        self.q = mqlightQueue(config)
        self.doStats = 0
        self.stats = {
            'domains' : 0,
            'startTime': 0,
            'endTime' : 0,
            'runningSeconds': 0,
            'avg': []
        }

    def callbackRabbit(self,ch, method, properties, body):
        start = datetime.now()
        domains = json.loads(body)

        message = self.resolveDomains(domains)

        ch.basic_publish(exchange='',routing_key='domains',body=message)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        nownow = datetime.now()

        if self.doStats:
            updateStats(start, len(domains), nownow)

        if len(domains) < self.packetSize:
            raise IOError

    def callbackMQL(self, type, body, delivery):
        start = datetime.now()
        domains = json.loads(body)
        # logger.info("Got %s domains" % len(domains))
        message = self.resolveDomains(domains)

        self.q.send('domains', message)
        delivery['message']['confirm_delivery']()
        nownow = datetime.now()

        if self.doStats:
            updateStats(start, len(domains), nownow)

        if len(domains) < self.packetSize:
            raise IOError

    def resolveDomains(self, domains):
        start = datetime.now()
        workQueue = Queue.Queue()
        fakeQueue = []
        threadId = 0
        for domain in domains:
            threadId = threadId + 1 
            thread = domainThread(domain,workQueue, threadId)
            thread.start()

        for x in range(len(domains)):
            domain = workQueue.get()
            fakeQueue.append(domain)

        message = json.dumps(fakeQueue)
        return message


    def updateStats(self, startTime, domainCount, endTime):
        elapsed = endTime - startTime
        if (elapsed.total_seconds() > 0):
            ds = round(domainCount / elapsed.total_seconds())
        else:
            ds = 0
        logger.info("resolved %s domains in %ss - %s d/s" % (domainCount, elapsed.total_seconds(), ds ))
        self.stats['domains'] = self.stats['domains'] + domainCount
        self.stats['runningSeconds'] =self.stats['runningSeconds'] + elapsed.total_seconds()
        self.stats['avg'].append(ds)
        self.stats['endTime'] = nownow.isoformat()


    def gogo(self,pid):
        while True:
            try:
                self.mainProc(pid)
            except BaseException as e:
                logger.exception(str(e))
            logger.info("There was an error CONSUMING. Sleeping for 600")
            time.sleep(600)

    def singleRun(self):

        logger.info("Starting up")
        start = datetime.now()
        self.doStats = 1
        self.stats['startTime'] = start
        # self.channel.queue_declare(queue='domains')
        # self.channel.queue_declare(queue='domain-queue')
        # self.channel.basic_consume(self.callback, queue='domain-queue')

        # channel.basic_qos(prefetch_count=1)
        # try:
        #     self.channel.start_consuming()
        # except KeyboardInterrupt:
        #     self.channel.stop_consuming()
        #     self.channel.stop_consuming()

        self.q.subscribe('domain-queue',self.callbackMQL)


        self.q.close()

        logger.info("Start: %s" % (self.stats['startTime']))
        logger.info("Ddomains: %s" % (self.stats['domains']))
        logger.info("runningSeconds: %s" % (self.stats['runningSeconds']))
        logger.info("Average domains/s %s" % (self.stats['avg']))
        logger.info("End: %s" % (self.stats['endTime']))



    def mainProc(self,pid):
        logger.info("%s Starting up", pid)
        start = datetime.now()
        # channel = self.connection.channel()
        # self.channel.queue_declare(queue='domains')
        # self.channel.queue_declare(queue='domain-queue')
        # self.channel.basic_consume(self.callback, queue='domain-queue')
        # # channel.basic_qos(prefetch_count=1)

        # self.channel.start_consuming()
        # self.pika_conn.close()


if __name__ == "__main__":
    logger.basicConfig(filename="resolver.log", format='%(asctime)s, %(message)s' ,level=logger.INFO)
    configFile = './config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    maxProcs = config.getint('domainResolver','processes')
    resolver = domainResolver()
    for x in range(maxProcs):
        Process(target=resolver.gogo,args=(x,)).start()





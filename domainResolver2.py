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
        logger.info("%s - %s - %s" % ( thisZone, zoneIp, self.threadId))
        workQueue.put(domain)
        return True

class domainResolver():
    def __init__():
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

    def callback(ch, method, properties, body):
        start = datetime.now()
        domains = json.loads(body)
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
        ch.basic_publish(exchange='',routing_key='domains',body=message)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        nownow = datetime.now()
        elapsed = nownow - start
        if (elapsed.total_seconds() > 0):
            ds = round(threadId / elapsed.total_seconds())
        else:
            ds = 0
        logger.info("resolved %s domains in %ss - %s d/s" % (threadId, elapsed.total_seconds(), ds ))

    def gogo(self,pid):
        while True:
            try:
                self.mainProc(pid)
            except BaseException as e:
                logger.exception(str(e))
            logger.info("There was an error CONSUMING. Sleeping for 600")
            time.sleep(600)

    def singleRun(pid):

        logger.info("%s Starting up", pid)
        start = datetime.now()

        self.channel.channel.queue_declare(queue='domains')
        self.channel.channel.queue_declare(queue='domain-queue')
        self.channel.channel.basic_consume(callback, queue='domain-queue')
        self.channel.channel.add_callback(stopRunning,pika.spec.Basic.GetEmpty)
        # channel.basic_qos(prefetch_count=1)

        self.channel.start_consuming()
        self.pika_conn.close()

    def stopRunning(frame):
        logger.info("Hit an empty Queue")
        self.channel.basic_cancel()
        self.pika_conn.close()

    def mainProc(pid):
        logger.info("%s Starting up", pid)
        start = datetime.now()
        channel = self.connection.channel()
        self.channel.channel.queue_declare(queue='domains')
        self.channel.channel.queue_declare(queue='domain-queue')
        self.channel.channel.basic_consume(callback, queue='domain-queue')
        # channel.basic_qos(prefetch_count=1)

        self.channel.channel.start_consuming()
        self.pika_conn.close()


if __name__ == "__main__":
    logger.basicConfig(filename="resolver.log", format='%(asctime)s, %(message)s' ,level=logger.INFO)
    configFile = './config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    maxProcs = config.getint('domainResolver','processes')
    resolver = domainResolver()
    for x in range(maxProcs):
        Process(target=resolver.gogo,args=(x,)).start()





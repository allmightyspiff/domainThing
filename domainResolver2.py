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
        logger.info("%s -  %s - %s - %s" % (nownow.isoformat(), thisZone, zoneIp, self.threadId))
        workQueue.put(domain)
        return True

def callback(ch, method, properties, body):
    domains = json.loads(body)
    workQueue = Queue.Queue()
    fakeQueue = []
    threadId = 0
    for domain in domains:
        thread = domainThread(domain,workQueue, threadId)
        thread.start()
        threadId = threadId + 1 

    for x in range(len(domains)):
        domain = workQueue.get()
        
        fakeQueue.append(domain)
    nownow = datetime.now()
    logger.info("%s - uploading to domains" % nownow.isoformat())
    message = json.dumps(fakeQueue)
    ch.basic_publish(exchange='',routing_key='domains',body=message)
    nownow = datetime.now()
    ch.basic_ack(delivery_tag = method.delivery_tag)

def main(pid):
    logger.info("%s Starting up", pid)
    start = datetime.now()
    configFile = './config.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    while True:
        credentials = pika.PlainCredentials(
                    config.get('rabbitmq','user'), 
                    config.get('rabbitmq','password')
                )
        params = pika.ConnectionParameters(
                    config.get('rabbitmq','host'), 
                    config.get('rabbitmq','port'), 
                    config.get('rabbitmq','vhost'), 
                    credentials=credentials,
                    channel_max=6,
                    heartbeat_interval=500,
                    connection_attempts=3,
                    socket_timeout=15
                )
        connection = pika.BlockingConnection(params)

        channel = connection.channel()
        channel.queue_declare(queue='domains')
        channel.queue_declare(queue='domain-queue')
        channel.basic_consume(callback, queue='domain-queue')
        channel.basic_qos(prefetch_count=1)

        try:
            channel.start_consuming()
            connection.close()
        except pika.exceptions.ConnectionClosed:
            nownow = datetime.now()
            print("%s - Retry Connection" % nownow.isoformat())
            continue
        time.sleep(1)

if __name__ == "__main__":
    logger.basicConfig(filename="resolver.log", format='%(asctime)s, %(message)s' ,level=logger.INFO)
    x = 0
    configFile = './config.cfg'
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    maxProcs = config.get('domainResolver','processes')
    while x <= maxProcs:
        x = x+1;
        Process(target=main,args=(x,)).start()
        time.sleep(5)




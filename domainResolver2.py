#!/usr/bin/env python
import pika
import json
import socket
from datetime import datetime, timedelta
from pprint import pprint as pp
import time
import logging as logger
#from multiprocessing import Process, Queue, current_process, active_children
import Queue
import threading


class domainThread(threading.Thread):

    def __init__(self, domain, queue, threadId):
        threading.Thread.__init__(self)
        self.domain = domain
        self.queue = queue
        self.threadId = threadId

    def run(self):
        self.processDomain(self.domain,self.queue)

    def getZoneIp(self,zone):
        ip = None
        try:
            query_result = socket.getaddrinfo(zone,'80')
            for result in query_result:
                ip = result[4][0]
                # print ip
            # pp(query_result)
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
        print("%s -  %s - %s - %s" % (nownow.isoformat(), thisZone, zoneIp, self.threadId))
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
        # Process(target=processDomain, args=(domain, workQueue)).start()

    for x in range(len(domains)):
        domain = workQueue.get()
        
        fakeQueue.append(domain)
    nownow = datetime.now()
    print("%s - uploading to domains" % nownow.isoformat())
    # active_children()
    message = json.dumps(fakeQueue)
    # pp(message)
    ch.basic_publish(exchange='',routing_key='domains',body=message)
    nownow = datetime.now()
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print("%s - Waiting" % nownow.isoformat())



logger.info("Starting up")
start = datetime.now()
print ' [*] Waiting for messages. To exit press CTRL+C'

# RabbitMQ likes to disconnect us. Might need to add a exit counter
# or something
while True:

    credentials = pika.PlainCredentials('domainThing', 'thisDomainThingy')
    params = pika.ConnectionParameters(
                   host='173.193.23.40',
                   port=5672,
                   virtual_host='/',
                   credentials=credentials,
                   channel_max=3,
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


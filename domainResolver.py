#!/usr/bin/env python
import pika
import json
import socket
from datetime import datetime, timedelta
import time
import logging as logger


def getZoneIp(zone):
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
    return ip


def callback(ch, method, properties, body):
    domains = json.loads(body)
    workQueue = []
    for domain in domains:
        start = datetime.now()
        thisZone = domain['domain']
        

        zoneIp = getZoneIp(thisZone)
        if zoneIp is None:
            zoneIp = getZoneIp("www." + thisZone)
            domain['domain'] = "www." + thisZone
        if zoneIp is None:
            zoneIp = "UNRESOLVEABLE"

        nownow = datetime.now()
        elapsed = nownow - start
        domain['ip'] = zoneIp
        domain['resolveTime'] = elapsed.total_seconds()
        domain['ipCreateTime'] = nownow.isoformat()
        workQueue.append(domain)
        print("%s -  %s - %s" % (nownow.isoformat(), thisZone, zoneIp))

    nownow = datetime.now()
    print("%s - uploading to domains" % nownow.isoformat())

    message = json.dumps(workQueue)
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
                   connection_attempts=3
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


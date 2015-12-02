#!/usr/bin/env python
import re
import socket
import os.path
import os
import sys
from pprint import pprint as pp
import pika
import json
from datetime import datetime, timedelta
import logging as logger
import time
import configparser 


class domainReader():

    def __init__(self):
        self.start = datetime.now()
        configFile = './config.cfg'
        config = configparser.ConfigParser()
        config.read(configFile)


        logger.info("domainReader Starting up")
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
        self.channel = connection.channel()
        self.channel.queue_declare(queue='domain-queue')

    def __exit__(self):
        logger.info("domainReader Shutting down")
        self.connection.close()

    def getZoneFiles(self, regex, path="./zones/icaan", startLine=0):
        for root, dirs, files in os.walk(path, topdown=True):
            for name in files:
                logger.info("Found FILE %s" % name)
                self.queueDomains(regex,os.path.join(root, name), startLine)


    def queueDomains(self,regex, filename, startLine):
        lastZone = ''
        lineNumber = 0
        workQueue = []
        queueLength = 0
        f = open(filename,'r')
        # Verisign zones don't end with the TLD
        # we can figure this out from the filename though
        nownow = datetime.now()
        tld = re.search("\S+\/(\S+)\.zone$", filename)
        for line in f:
            lineNumber = lineNumber + 1
            if lineNumber < startLine:
                continue
            zone = regex.match(line)
            if zone:
                thisZone = zone.group(1)
                if tld:
                    thisZone = thisZone + "." + tld.group(1)

                # Most zones have multiple entries, we only care abotu the first
                if thisZone == lastZone:
                    continue
                
                lastZone = thisZone
                nownow = datetime.now()

                zoneObject = {
                    'created': nownow.isoformat(),
                    'domain' : lastZone,
                    'domainFullZone': zone.group(0)
                }
                workQueue.append(zoneObject)
                queueLength = queueLength + 1

            if  queueLength > 25:
                self.uploadQueue(workQueue)
                logger.info("%s - %s" % (lineNumber, thisZone))
                queueLength = 0
                workQueue = []
                # Sleeping to not overload queue
                # need to replace with something more aware
                time.sleep(.1)
        self.uploadQueue(workQueue)
        nownow = datetime.now()
        logger.info("%s - Finished with %s" % (nownow.isoformat(),filename))


    def uploadQueue(self, workQueue):
        nownow = datetime.now()
        message = json.dumps(workQueue)
        self.channel.basic_publish(exchange='', routing_key='domain-queue', body=message)


if __name__ == "__main__":
    logger.basicConfig(filename="parser.log", format='%(asctime)s, %(message)s' ,level=logger.INFO)
    regexIcaan = re.compile('(\S+)\.\s+(\d+)\s+in\s+ns\s+(\S*)')
    regexVerisign = re.compile('(\S+)(\s+NS\s+)(\S*)')
    regexORG = re.compile('(\S+)\.(\s+NS\s+)(\S*)')
    
    configFile = './config.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    ready = config.getint('domainParser','ready')
    while not ready:
        logger.info("Not ready, sleeping for 60")
        time.sleep(60)
        config.read(configFile)
        ready = config.getint('domainParser','ready')

    try:

        domainReader = domainReader()
        domainReader.getZoneFiles(regexVerisign, "./zones/verisign")
        domainReader.getZoneFiles(regexIcaan, "./zones/icaan")
        domainReader.getZoneFiles(regexORG, "./zones/org")
    except BaseException as e:
        logger.error("Exiting due to exception")
        logger.exception(str(e))




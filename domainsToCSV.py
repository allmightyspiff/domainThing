import elasticsearch
from pprint import pprint as pp
import time
from datetime import datetime, timedelta
import sys


def printDomain(domains):
    for domain in domains:
        hostname = domain['fields']['domain'][0]
        ip = domain['fields']['ip'][0]
        print("\"%s\", \"%s\"" % (hostname,ip))

es = elasticsearch.Elasticsearch([{'host':'10.37.82.159'}])
nextNumber = 500
startNumber = 0
print("domain, ip")
softlayer  = es.search(index='domain-final', q="softlayer:1", fields="domain,ip",from_=startNumber, size=nextNumber)
#pp(softlayer)
printDomain(softlayer['hits']['hits'])
total = softlayer['hits']['total']
while(startNumber <= total):
    startNumber = startNumber + nextNumber
    softlayer  = es.search(index='domain-final', q="softlayer:1", fields="domain,ip",from_=nextNumber, size=startNumber)
    printDomain(softlayer['hits']['hits'])


pp(softlayer)
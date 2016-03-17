from domainParser import domainReader
from domainResolver2 import domainResolver
from domainConsumer import domainConsumer
import logging 


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(3)
    print("Starting to resolve")
    resolver = domainResolver()
    resolver.singleRun()
    print("Getting some zone data")
    reader = domainReader('verisign', 1)
    reader.getZoneFiles()
    reader.printStats()

    print("DONE RESOLVING")
    consumer = domainConsumer("testing-1")
    consumer.singleRun()
    print("DONE")

from domainParser import domainReader
from domainResolver2 import domainResolver
from domainConsumer import domainConsumer
import logging as logger


if __name__ == "__main__":
    logger.basicConfig(format='%(asctime)s, %(message)s' ,level=logger.INFO)
    print("Getting some zone data")
    reader = domainReader('verisign')
    # reader.getZoneFiles()
    print("Starting to resolve")
    resolver = domainResolver()
    resolver.singleRun()
    print("DONE RESOLVING")
    consumer = domainConsumer("testing-1")
    consumer.main()
    print("DONE")

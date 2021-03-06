from domainParser import domainReader
from domainResolver2 import domainResolver
from domainConsumer import domainConsumer
import logging 
from multiprocessing import Process, current_process, active_children

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(3)
    print("Starting to resolve")
    # resolver = domainResolver()
    # Process(target=resolver.singleRun).start()
    print("===============================")
    print("Getting some zone data")
    reader = domainReader('verisign', 1)
    # Process(target=reader.getZoneFiles).start()
    reader.getZoneFiles()
    print("===============================")

    print("DONE RESOLVING")
    #consumer = domainConsumer("testing-1")
    #consumer.singleRun()
    print("DONE")
    # active_children()
    # exit(0)

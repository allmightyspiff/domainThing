from domainParser import domainReader
from domainResolver2 import mainProc
import logging as logger


if __name__ == "__main__":
    logger.basicConfig(format='%(asctime)s, %(message)s' ,level=logger.INFO)
    print("Getting some zone data")
    reader = domainReader('verisign')
    # reader.getZoneFiles()
    print("Starting to resolve")
    mainProc(1)
    print("DONE")
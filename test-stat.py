import elasticsearch
from pprint import pprint as pp
import time
from datetime import datetime, timedelta
import sys

es = elasticsearch.Elasticsearch([{'host':'10.37.82.159'}])
last = 0
now = 0
lastTime = datetime.now()
print("Time,Non SL, Yes SL, Rate")
time.sleep(1)
while True:
	matchesNO = es.search(index='domain-final', q="softlayer:0")
	matchesYES = es.search(index='domain-final', q="softlayer:1")
	noCount = matchesNO['hits']['total']
	yesCount = matchesYES['hits']['total']
	now = noCount + yesCount
	if last == 0:
		last = now
		continue
	thisTime = datetime.now()
	elapsed = thisTime - lastTime
	#print("%s" % elapsed.total_seconds() )
	rate = round((now - last) / round(elapsed.total_seconds()),2)
	print("%s,%s,%s,%s/s" % (time.time(),noCount,yesCount,rate))
	lastTime = datetime.now()
	last = now
	sys.stdout.flush()
	time.sleep(60)
	#time.sleep(10)



